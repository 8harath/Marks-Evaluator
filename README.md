# Academic Essay Evaluation Platform

A Flask-based web application for automated evaluation of student essays using Google's Gemini AI.

## Project Overview

This platform was developed to enhance the essay evaluation process at Jain University. It replaces manual grading with an AI-powered system that assesses student submissions on relevance, coverage, and structure.

## Features

- User Authentication with role-based access (faculty/student)
- Faculty Dashboard for creating questions and managing submissions
- Student Interface for submitting answers and viewing feedback
- AI Evaluation using Google's Gemini 1.5 Pro model
- Interactive UI with animations and data visualization
- Multiline Text Support across all interfaces
- PDF Report Generation with properly formatted text
- Database support for both SQLite and PostgreSQL

## Technology Stack

- Backend: Python 3, Flask framework
- Database: SQLite (development) / PostgreSQL (production)
- ORM: SQLAlchemy with polymorphic models
- Authentication: Flask-Login
- Forms: Flask-WTF, WTForms
- AI: Google Generative AI (Gemini API)
- Frontend: HTML, CSS, JavaScript, Bootstrap 5
- Charts: Chart.js
- Animations: AOS Animation Library

## Installation

### Prerequisites

- Python 3.8+
- PostgreSQL (optional for production)
- Google Gemini API key

### Setup Steps

1. Clone the repository
2. Create and activate a virtual environment
3. Install dependencies: `pip install -r requirements.txt`
4. Configure environment variables in a `.env` file:
   ```
   DATABASE_URL=sqlite:///essay_evaluation.db
   GOOGLE_API_KEY=your_gemini_api_key
   SESSION_SECRET=your_secret_key
   ```
5. Run the application:
   ```bash
   python main.py
   # Or for production
   gunicorn --bind 0.0.0.0:5000 main:app
   ```
6. Access at http://localhost:5000

### Running on Replit

1. The application uses PostgreSQL via the DATABASE_URL environment variable
2. Set the GOOGLE_API_KEY in Replit Secrets
3. The application will start automatically via the workflow

## Using the Application

### For Faculty
1. Register as faculty
2. Create questions with reference answers
3. Set word limits and maximum marks
4. Evaluate submissions with AI
5. View results and generate PDF reports

### For Students
1. Register as student
2. Browse questions
3. Submit answers with proper formatting
4. View feedback and scores

### Multiline Text Support
The application properly renders paragraphs and line breaks across all interfaces:
- Questions and reference answers
- Student submissions
- AI feedback
- PDF reports

## Google Gemini API Setup
1. Get an API key from [Google AI Studio](https://ai.google.dev/)
2. Add it to your environment as GOOGLE_API_KEY
3. The application uses the gemini-1.5-pro model

## Troubleshooting

- Database Issues: Check connection strings and permissions
- API Errors: Verify your Gemini API key is valid
- Template Errors: Check for missing variables in route handlers

## Performance Notes
- Each AI evaluation takes 10-15 seconds
- Best suited for classes of up to 100 students
- Consider batch processing for larger deployments

## License
MIT License

## Credits
Developed for Jain University's academic evaluation system
