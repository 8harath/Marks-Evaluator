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
    content.append(Paragraph(f"<b>Question:</b> {question.text}", normal_style))
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
