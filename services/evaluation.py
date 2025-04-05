import os
import google.generativeai as genai
from app import db
from models import Evaluation
import logging

# Set up the Gemini API
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY", "")

def evaluate_submissions(submissions, question):
    """
    Evaluate student submissions against a reference key answer using Gemini API.
    
    Args:
        submissions: List of Submission objects to evaluate
        question: The Question object with the key answer
    
    Returns:
        None (evaluations are saved to the database)
    """
    if not GOOGLE_API_KEY:
        logging.error("GOOGLE_API_KEY environment variable is not set")
        raise ValueError("GOOGLE_API_KEY is not set in environment variables. Please configure a valid API key.")
    
    # Configure the API with the current key - do this each time to ensure we use the latest key
    try:
        genai.configure(api_key=GOOGLE_API_KEY)
        # Configure the model
        model = genai.GenerativeModel('gemini-1.5-pro')
    except Exception as e:
        logging.error(f"Error configuring Gemini API: {str(e)}")
        raise ValueError(f"Failed to initialize Gemini API: {str(e)}")
    
    for submission in submissions:
        # Skip if already evaluated
        if hasattr(submission, 'evaluation') and submission.evaluation:
            logging.info(f"Submission {submission.id} already evaluated, skipping")
            continue
        
        # Construct the prompt for Gemini
        prompt = f"""
        Given a reference answer and a student's response, evaluate the submission on a scale of 0-100 based on three criteria:
        
        1) Relevance to the question and alignment with the reference answer;
        2) Coverage of key points and completeness relative to the reference;
        3) Structure, coherence, and clarity of expression.
        
        Return the evaluation in a structured format with a score for each criterion and a total score.
        
        Question: {question.text}
        
        Reference answer: {question.key_answer}
        
        Student's response: {submission.answer_text}
        
        Provide your evaluation in this exact format:
        Relevance score: [0-100]
        Coverage score: [0-100]
        Structure score: [0-100]
        Total score: [0-100]
        Feedback: [brief justification for each criterion]
        """
        
        try:
            # Call the Gemini API
            response = model.generate_content(prompt)
            
            # Parse the response
            response_text = response.text
            
            # Extract scores and feedback using parsing
            lines = response_text.strip().split('\n')
            
            # Initialize values
            relevance_score = 0
            coverage_score = 0
            structure_score = 0
            total_score = 0
            feedback = ""
            
            # Parse each line to extract scores and feedback
            for line in lines:
                if "Relevance score:" in line:
                    relevance_score = float(line.split(':')[1].strip().split()[0])
                elif "Coverage score:" in line:
                    coverage_score = float(line.split(':')[1].strip().split()[0])
                elif "Structure score:" in line:
                    structure_score = float(line.split(':')[1].strip().split()[0])
                elif "Total score:" in line:
                    total_score = float(line.split(':')[1].strip().split()[0])
                elif "Feedback:" in line:
                    feedback = line.split(':', 1)[1].strip()
                    # Also gather any remaining lines as part of feedback
                    feedback_start_idx = lines.index(line) + 1
                    if feedback_start_idx < len(lines):
                        additional_feedback = '\n'.join(lines[feedback_start_idx:])
                        feedback = f"{feedback}\n{additional_feedback}"
            
            # Scale to max_marks if needed
            if question.max_marks != 100:
                total_score = (total_score / 100) * question.max_marks
            
            # Create and save evaluation
            evaluation = Evaluation(
                relevance_score=relevance_score,
                coverage_score=coverage_score,
                structure_score=structure_score,
                total_score=total_score,
                feedback=feedback,
                submission_id=submission.id
            )
            
            db.session.add(evaluation)
            db.session.commit()
            logging.info(f"Successfully evaluated submission {submission.id}")
            
        except Exception as e:
            logging.error(f"Error evaluating submission {submission.id}: {str(e)}")
            raise
