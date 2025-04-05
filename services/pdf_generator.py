from flask import make_response
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from io import BytesIO
from datetime import datetime
import os
import logging

def generate_results_pdf(question, evaluations):
    """
    Generate a PDF report for evaluation results.
    
    Args:
        question: The Question object
        evaluations: List of Evaluation objects with their related submissions
    
    Returns:
        PDF file as Flask response
    """
    buffer = BytesIO()
    
    # Create PDF document
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        name='TitleStyle',
        parent=styles['Heading1'],
        fontSize=16,
        spaceAfter=12,
        alignment=1  # Center
    )
    
    subtitle_style = ParagraphStyle(
        name='SubtitleStyle',
        parent=styles['Heading2'],
        fontSize=14,
        spaceAfter=8
    )
    
    normal_style = styles['Normal']
    normal_style.fontSize = 10
    
    # Build document content
    content = []
    
    # Add Jain University logo - use SVG text instead of actual image file
    logo_path = "static/assets/jain_university_logo.svg"
    if os.path.exists(logo_path):
        img = Image(logo_path, width=2*inch, height=0.75*inch)
        content.append(img)
    
    # Add title and date
    content.append(Paragraph("Evaluation Results Report", title_style))
    content.append(Paragraph(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M')}", normal_style))
    content.append(Spacer(1, 12))
    
    # Add question details
    content.append(Paragraph("Question Details", subtitle_style))
    # Replace newlines with HTML line breaks for proper PDF rendering
    formatted_question_text = question.text.replace('\n', '<br/>')
    content.append(Paragraph(f"<b>Question:</b> {formatted_question_text}", normal_style))
    content.append(Paragraph(f"<b>Word Limit:</b> {question.word_limit}", normal_style))
    content.append(Paragraph(f"<b>Maximum Marks:</b> {question.max_marks}", normal_style))
    content.append(Spacer(1, 12))
    
    # Add results table
    content.append(Paragraph("Student Results", subtitle_style))
    
    # Create table data
    table_data = [
        ['Rank', 'Student Name', 'Score', 'Relevance', 'Coverage', 'Structure', 'Submission Time']
    ]
    
    for evaluation in evaluations:
        submission = evaluation.submission
        student = submission.student
        
        table_data.append([
            evaluation.rank or '-',
            student.username,
            f"{evaluation.total_score:.1f}",
            f"{evaluation.relevance_score:.1f}",
            f"{evaluation.coverage_score:.1f}",
            f"{evaluation.structure_score:.1f}",
            submission.submitted_at.strftime('%Y-%m-%d %H:%M')
        ])
    
    # Create table
    table = Table(table_data, repeatRows=1)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    content.append(table)
    content.append(Spacer(1, 12))
    
    # Add key answer
    content.append(Paragraph("Key Answer (Reference Solution)", subtitle_style))
    formatted_key_answer = question.key_answer.replace('\n', '<br/>')
    content.append(Paragraph(formatted_key_answer, normal_style))
    content.append(Spacer(1, 12))
    
    # Add detailed breakdown of submissions
    content.append(Paragraph("Submission Details", subtitle_style))
    
    for i, evaluation in enumerate(evaluations):
        submission = evaluation.submission
        student = submission.student
        
        content.append(Paragraph(f"<b>{i+1}. {student.username}</b> (Score: {evaluation.total_score:.1f}, Rank: {evaluation.rank or '-'})", 
                                  ParagraphStyle(name='SubmissionHeader', parent=normal_style, fontName='Helvetica-Bold')))
        
        # Format student's answer with line breaks
        formatted_answer = submission.answer_text.replace('\n', '<br/>')
        content.append(Paragraph(formatted_answer, normal_style))
        
        # Add feedback if available
        if evaluation.feedback:
            content.append(Paragraph("<b>AI Feedback:</b>", normal_style))
            formatted_feedback = evaluation.feedback.replace('\n', '<br/>')
            content.append(Paragraph(formatted_feedback, 
                                     ParagraphStyle(name='FeedbackStyle', parent=normal_style, leftIndent=20)))
        
        content.append(Spacer(1, 12))
    
    # Add statistics
    if evaluations:
        avg_score = sum(e.total_score for e in evaluations) / len(evaluations)
        highest_score = max(e.total_score for e in evaluations)
        lowest_score = min(e.total_score for e in evaluations)
        
        content.append(Paragraph("Statistics", subtitle_style))
        content.append(Paragraph(f"<b>Number of Submissions:</b> {len(evaluations)}", normal_style))
        content.append(Paragraph(f"<b>Average Score:</b> {avg_score:.1f}", normal_style))
        content.append(Paragraph(f"<b>Highest Score:</b> {highest_score:.1f}", normal_style))
        content.append(Paragraph(f"<b>Lowest Score:</b> {lowest_score:.1f}", normal_style))
        content.append(Spacer(1, 12))
    
    # Add footer
    footer_text = "This project is built by a student from Jain University"
    content.append(Paragraph(footer_text, ParagraphStyle(
        name='Footer',
        parent=styles['Normal'],
        fontSize=8,
        textColor=colors.grey,
        alignment=1  # Center
    )))
    
    # Build the PDF
    doc.build(content)
    
    # Create response
    buffer.seek(0)
    response = make_response(buffer.getvalue())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'attachment; filename=results_{question.id}.pdf'
    
    return response
