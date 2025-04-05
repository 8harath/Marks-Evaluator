from flask import Blueprint, render_template, url_for, flash, redirect, request, abort
from flask_login import current_user, login_required
from app import db
from sqlalchemy import func
from models import Question, Submission, Evaluation, Student
from forms import QuestionForm
from flask_wtf import FlaskForm
from services.evaluation import evaluate_submissions
from services.pdf_generator import generate_results_pdf
import logging
import google.generativeai as genai
import os

faculty_bp = Blueprint('faculty', __name__, url_prefix='/faculty')

# Faculty route protection middleware
@faculty_bp.before_request
def check_faculty():
    if not current_user.is_authenticated or current_user.role != 'faculty':
        abort(403)  # Forbidden

@faculty_bp.route('/dashboard')
@login_required
def dashboard():
    # Get all questions created by the faculty
    questions = Question.query.filter_by(faculty_id=current_user.id).order_by(Question.created_at.desc()).all()
    
    # For each question, get the number of submissions
    questions_data = []
    for question in questions:
        submission_count = Submission.query.filter_by(question_id=question.id).count()
        evaluated_count = Submission.query.join(Evaluation).filter(Submission.question_id == question.id).count()
        
        questions_data.append({
            'question': question,
            'submission_count': submission_count,
            'evaluated_count': evaluated_count
        })
    
    return render_template('faculty/dashboard.html', 
                           title='Faculty Dashboard', 
                           questions_data=questions_data)

@faculty_bp.route('/question/new', methods=['GET', 'POST'])
@login_required
def create_question():
    form = QuestionForm()
    if form.validate_on_submit():
        question = Question(
            text=form.text.data,
            key_answer=form.key_answer.data,
            word_limit=form.word_limit.data,
            max_marks=form.max_marks.data,
            faculty_id=current_user.id
        )
        db.session.add(question)
        db.session.commit()
        flash('Your question has been created!', 'success')
        return redirect(url_for('faculty.dashboard'))
    
    return render_template('faculty/create_question.html', 
                           title='Create Question', 
                           form=form,
                           legend='Create a New Question')

@faculty_bp.route('/question/<int:question_id>')
@login_required
def view_question(question_id):
    question = Question.query.get_or_404(question_id)
    
    # Ensure the faculty is the owner of the question
    if question.faculty_id != current_user.id:
        abort(403)
    
    # Get all submissions for this question
    submissions = Submission.query.filter_by(question_id=question.id).all()
    
    # Check if all submissions have been evaluated
    all_evaluated = all(submission.evaluation is not None for submission in submissions)
    
    # Create a simple form for CSRF protection
    form = FlaskForm()
    
    return render_template('faculty/view_question.html', 
                           title='Question Details', 
                           question=question,
                           submissions=submissions,
                           all_evaluated=all_evaluated,
                           form=form)

@faculty_bp.route('/question/<int:question_id>/update', methods=['GET', 'POST'])
@login_required
def update_question(question_id):
    question = Question.query.get_or_404(question_id)
    
    # Ensure the faculty is the owner of the question
    if question.faculty_id != current_user.id:
        abort(403)
    
    form = QuestionForm()
    if form.validate_on_submit():
        question.text = form.text.data
        question.key_answer = form.key_answer.data
        question.word_limit = form.word_limit.data
        question.max_marks = form.max_marks.data
        db.session.commit()
        flash('Your question has been updated!', 'success')
        return redirect(url_for('faculty.view_question', question_id=question.id))
    elif request.method == 'GET':
        form.text.data = question.text
        form.key_answer.data = question.key_answer
        form.word_limit.data = question.word_limit
        form.max_marks.data = question.max_marks
    
    return render_template('faculty/create_question.html', 
                           title='Update Question', 
                           form=form,
                           legend='Update Question')

@faculty_bp.route('/question/<int:question_id>/delete', methods=['POST'])
@login_required
def delete_question(question_id):
    question = Question.query.get_or_404(question_id)
    
    # Ensure the faculty is the owner of the question
    if question.faculty_id != current_user.id:
        abort(403)
    
    db.session.delete(question)
    db.session.commit()
    flash('Your question has been deleted!', 'success')
    return redirect(url_for('faculty.dashboard'))

@faculty_bp.route('/question/<int:question_id>/evaluate', methods=['POST'])
@login_required
def evaluate_question(question_id):
    question = Question.query.get_or_404(question_id)
    
    # Ensure the faculty is the owner of the question
    if question.faculty_id != current_user.id:
        abort(403)
    
    # Get all unevaluated submissions for this question
    submissions = Submission.query.filter_by(question_id=question.id).all()
    submissions_to_evaluate = [s for s in submissions if s.evaluation is None]
    
    if not submissions_to_evaluate:
        flash('All submissions for this question have already been evaluated.', 'info')
        return redirect(url_for('faculty.view_question', question_id=question.id))
    
    try:
        # Evaluate the submissions using Gemini API
        evaluate_submissions(submissions_to_evaluate, question)
        
        # Update the ranks
        all_evaluations = Evaluation.query.join(Submission).filter(
            Submission.question_id == question.id
        ).order_by(Evaluation.total_score.desc()).all()
        
        for i, eval in enumerate(all_evaluations):
            eval.rank = i + 1
        
        db.session.commit()
        flash(f'Successfully evaluated {len(submissions_to_evaluate)} submissions!', 'success')
    except ValueError as e:
        # Specific error for API key issues
        logging.error(f"API key error during evaluation: {str(e)}")
        db.session.rollback()
        if "API key" in str(e):
            flash('Evaluation failed: The Google Gemini API key is invalid or missing. Please contact the administrator to set up a valid API key.', 'danger')
        else:
            flash(f'Error during evaluation: {str(e)}', 'danger')
    except Exception as e:
        logging.error(f"Evaluation error: {str(e)}")
        db.session.rollback()
        flash(f'Error during evaluation: {str(e)}', 'danger')
    
    return redirect(url_for('faculty.results', question_id=question.id))

@faculty_bp.route('/question/<int:question_id>/results')
@login_required
def results(question_id):
    question = Question.query.get_or_404(question_id)
    
    # Ensure the faculty is the owner of the question
    if question.faculty_id != current_user.id:
        abort(403)
    
    # Get all evaluated submissions for this question
    evaluations = Evaluation.query.join(Submission).filter(
        Submission.question_id == question.id
    ).order_by(Evaluation.rank).all()
    
    if not evaluations:
        flash('No evaluated submissions found for this question.', 'info')
        return redirect(url_for('faculty.view_question', question_id=question.id))
    
    # Prepare data for chart (average scores by criterion)
    avg_relevance = db.session.query(func.avg(Evaluation.relevance_score)).join(Submission).filter(
        Submission.question_id == question.id
    ).scalar() or 0
    
    avg_coverage = db.session.query(func.avg(Evaluation.coverage_score)).join(Submission).filter(
        Submission.question_id == question.id
    ).scalar() or 0
    
    avg_structure = db.session.query(func.avg(Evaluation.structure_score)).join(Submission).filter(
        Submission.question_id == question.id
    ).scalar() or 0
    
    chart_data = {
        'labels': ['Relevance', 'Coverage', 'Structure'],
        'values': [avg_relevance, avg_coverage, avg_structure]
    }
    
    return render_template('faculty/results.html',
                           title='Evaluation Results',
                           question=question,
                           evaluations=evaluations,
                           chart_data=chart_data)

@faculty_bp.route('/question/<int:question_id>/generate_pdf')
@login_required
def generate_pdf(question_id):
    question = Question.query.get_or_404(question_id)
    
    # Ensure the faculty is the owner of the question
    if question.faculty_id != current_user.id:
        abort(403)
    
    # Get all evaluated submissions for this question
    evaluations = Evaluation.query.join(Submission).filter(
        Submission.question_id == question.id
    ).order_by(Evaluation.rank).all()
    
    if not evaluations:
        flash('No evaluated submissions found for this question.', 'info')
        return redirect(url_for('faculty.view_question', question_id=question.id))
    
    try:
        # Generate PDF
        pdf_data = generate_results_pdf(question, evaluations)
        return pdf_data
    except Exception as e:
        logging.error(f"PDF generation error: {str(e)}")
        flash(f'Error generating PDF: {str(e)}', 'danger')
        return redirect(url_for('faculty.results', question_id=question.id))

@faculty_bp.route('/api_status')
@login_required
def api_status():
    """Check the status of the Google Gemini API."""
    api_working = False
    error_message = "No error details available."
    
    try:
        # Get the API key from environment
        api_key = os.environ.get("GOOGLE_API_KEY", "")
        
        if not api_key:
            error_message = "Google Gemini API key is not set in environment variables. Please configure a valid API key."
        else:
            # Try to initialize the API
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-1.5-pro')
            
            # Send a simple test prompt
            test_prompt = "Hello, this is a test of the Google Gemini API. Please respond with 'API is working'."
            response = model.generate_content(test_prompt)
            
            # If we get here without an exception, the API is working
            api_working = True
    except Exception as e:
        error_message = str(e)
        logging.error(f"API status check error: {error_message}")
    
    return render_template('faculty/api_status.html',
                          title='API Status',
                          api_working=api_working,
                          error_message=error_message)

@faculty_bp.route('/test_api')
@login_required
def test_api():
    """Re-test the API connection."""
    return redirect(url_for('faculty.api_status'))
