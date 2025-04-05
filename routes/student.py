from flask import Blueprint, render_template, url_for, flash, redirect, request, abort, session
from flask_login import current_user, login_required, login_user
from app import db
from models import Question, Submission, Evaluation, Student, User
from forms import SubmissionForm, SimpleStudentForm
import logging

student_bp = Blueprint('student', __name__, url_prefix='/student')

@student_bp.route('/dashboard')
def dashboard():
    # Get all available questions
    questions = Question.query.order_by(Question.created_at.desc()).all()
    
    if current_user.is_authenticated and current_user.role == 'student':
        # For authenticated students, check if they've submitted answers
        submitted_question_ids = [sub.question_id for sub in current_user.submissions]
        
        # For each question, check if the student can still submit (limit of 5 submissions per question)
        questions_data = []
        for question in questions:
            submission_count = Submission.query.filter_by(question_id=question.id).count()
            can_submit = question.id not in submitted_question_ids and submission_count < 5
            has_submitted = question.id in submitted_question_ids
            
            # If student has submitted, get their evaluation if available
            evaluation = None
            if has_submitted:
                submission = Submission.query.filter_by(
                    student_id=current_user.id,
                    question_id=question.id
                ).first()
                
                if submission and submission.evaluation:
                    evaluation = submission.evaluation
            
            questions_data.append({
                'question': question,
                'submission_count': submission_count,
                'can_submit': can_submit,
                'has_submitted': has_submitted,
                'evaluation': evaluation
            })
        
        return render_template('student/dashboard.html', 
                            title='Student Dashboard', 
                            questions_data=questions_data)
    else:
        # For non-authenticated users, just show available questions
        questions_data = []
        for question in questions:
            submission_count = Submission.query.filter_by(question_id=question.id).count()
            can_submit = submission_count < 5
            
            questions_data.append({
                'question': question,
                'submission_count': submission_count,
                'can_submit': can_submit,
                'has_submitted': False,
                'evaluation': None
            })
        
        return render_template('student/dashboard.html', 
                            title='Available Questions', 
                            questions_data=questions_data)

@student_bp.route('/question/<int:question_id>')
def view_question(question_id):
    question = Question.query.get_or_404(question_id)
    
    # Check if the question already has 5 submissions
    submission_count = Submission.query.filter_by(question_id=question.id).count()
    if submission_count >= 5:
        flash('This question has reached the maximum number of submissions.', 'info')
        return redirect(url_for('student.dashboard'))
    
    # For authenticated students, check if they've already submitted
    if current_user.is_authenticated and current_user.role == 'student':
        submission = Submission.query.filter_by(
            student_id=current_user.id,
            question_id=question.id
        ).first()
        
        if submission:
            flash('You have already submitted an answer for this question.', 'info')
            return redirect(url_for('student.dashboard'))
    
    return render_template('student/view_question.html', 
                           title='Question Details', 
                           question=question)

@student_bp.route('/question/<int:question_id>/submit', methods=['GET', 'POST'])
def submit_answer(question_id):
    question = Question.query.get_or_404(question_id)
    
    # Check if the question already has 5 submissions
    submission_count = Submission.query.filter_by(question_id=question.id).count()
    if submission_count >= 5:
        flash('This question has reached the maximum number of submissions.', 'info')
        return redirect(url_for('student.dashboard'))
    
    # If user is authenticated as a student
    if current_user.is_authenticated and current_user.role == 'student':
        # Check if they've already submitted
        existing_submission = Submission.query.filter_by(
            student_id=current_user.id,
            question_id=question.id
        ).first()
        
        if existing_submission:
            flash('You have already submitted an answer for this question.', 'info')
            return redirect(url_for('student.dashboard'))
        
        form = SubmissionForm()
        if form.validate_on_submit():
            # Count words
            word_count = len(form.answer_text.data.split())
            
            # Validate word count against question limit
            if word_count > question.word_limit:
                flash(f'Your answer exceeds the word limit of {question.word_limit} words.', 'danger')
                return render_template('student/submit_answer.html', 
                                      title='Submit Answer', 
                                      form=form, 
                                      question=question)
            
            # Create submission
            submission = Submission(
                answer_text=form.answer_text.data,
                word_count=word_count,
                student_id=current_user.id,
                question_id=question.id
            )
            
            db.session.add(submission)
            db.session.commit()
            
            flash('Your answer has been submitted successfully!', 'success')
            return redirect(url_for('student.dashboard'))
        
        return render_template('student/submit_answer.html', 
                              title='Submit Answer', 
                              form=form, 
                              question=question)
    
    # For non-authenticated users, show simplified form
    else:
        # Check if there's a temporary student in session
        if 'temp_student' in session:
            # Use the temporary student info
            student_email = session['temp_student']['email']
            student = Student.query.filter_by(email=student_email).first()
            
            if not student:
                # Create a new student user
                username = session['temp_student']['name'].lower().replace(' ', '_')
                email = session['temp_student']['email']
                
                # Check if username already exists
                existing_user = User.query.filter_by(username=username).first()
                if existing_user:
                    username = f"{username}_{submission_count + 1}"
                
                student = Student(username=username, email=email)
                student.set_password('temporary')  # Simple password as they're not expected to log in
                db.session.add(student)
                db.session.commit()
                
                # Log the student in
                login_user(student)
            
            # Now show the submission form
            form = SubmissionForm()
            if form.validate_on_submit():
                # Count words
                word_count = len(form.answer_text.data.split())
                
                # Validate word count against question limit
                if word_count > question.word_limit:
                    flash(f'Your answer exceeds the word limit of {question.word_limit} words.', 'danger')
                    return render_template('student/submit_answer.html', 
                                          title='Submit Answer', 
                                          form=form, 
                                          question=question)
                
                # Create submission
                submission = Submission(
                    answer_text=form.answer_text.data,
                    word_count=word_count,
                    student_id=student.id,
                    question_id=question.id
                )
                
                db.session.add(submission)
                db.session.commit()
                
                # Clear temporary student from session
                session.pop('temp_student', None)
                
                flash('Your answer has been submitted successfully!', 'success')
                return redirect(url_for('student.dashboard'))
            
            return render_template('student/submit_answer.html', 
                                  title='Submit Answer', 
                                  form=form, 
                                  question=question)
        
        # Show form to get student details
        form = SimpleStudentForm()
        if form.validate_on_submit():
            # Store temporary student info in session
            session['temp_student'] = {
                'name': form.name.data,
                'email': form.email.data
            }
            
            return redirect(url_for('student.submit_answer', question_id=question.id))
        
        return render_template('student/register_temp.html', 
                              title='Your Information', 
                              form=form, 
                              question=question)

@student_bp.route('/results')
@login_required
def results():
    # This route is only accessible to authenticated students
    if current_user.role != 'student':
        abort(403)
    
    # Get all submissions by the student that have been evaluated
    evaluated_submissions = Submission.query.filter_by(
        student_id=current_user.id
    ).join(Evaluation).all()
    
    if not evaluated_submissions:
        flash('You have no evaluated submissions yet.', 'info')
        return redirect(url_for('student.dashboard'))
    
    # Prepare results data
    results_data = []
    for submission in evaluated_submissions:
        results_data.append({
            'question': submission.question,
            'submission': submission,
            'evaluation': submission.evaluation
        })
    
    return render_template('student/results.html',
                           title='My Results',
                           results_data=results_data)
