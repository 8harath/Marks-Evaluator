# Academic Essay Evaluation Platform

A Flask-based web application for automated evaluation of student essays using Google's Gemini AI. This platform provides tools for faculty to create essay questions and automatically evaluate student submissions across multiple dimensions, with special emphasis on text formatting and multiline content support.

## Project Overview

This platform was developed to enhance the essay evaluation process at Jain University. It replaces manual grading with an AI-powered system that assesses student submissions on relevance, coverage, and structure. Faculty members can create questions, view submissions, and generate detailed reports, while students can submit answers and receive comprehensive feedback.

## Features

- **User Authentication System**: Secure login and registration with role-based access (faculty/student)
- **Faculty Dashboard**: Create questions, view submissions, evaluate essays, generate PDF reports
- **Student Interface**: Browse available questions, submit answers, view feedback and scores
- **AI Evaluation**: Automated essay evaluation using Google's Generative AI (Gemini 1.5 Pro model)
- **Interactive UI**: Smooth animations, dynamic charts, and responsive design
- **Data Visualization**: Score distribution, performance comparison, and detailed feedback
- **Multiline Text Support**: Proper rendering of paragraphs and line breaks across all interfaces
- **PDF Reports**: Comprehensive reports with proper text formatting for questions, answers, and feedback
- **Database Flexibility**: Seamless support for both SQLite (development) and PostgreSQL (production)

## Technology Stack

- **Backend**: Python 3, Flask framework
- **Database**: SQLite (development) / PostgreSQL (production)
- **ORM**: SQLAlchemy with polymorphic models
- **Authentication**: Flask-Login with role-based access control
- **Forms**: Flask-WTF, WTForms with validation
- **AI Integration**: Google Generative AI (Gemini 1.5 Pro model)
- **PDF Generation**: ReportLab with custom styling
- **Frontend**: HTML, CSS, JavaScript
- **UI Framework**: Bootstrap 5 with dark theme
- **Charts**: Chart.js for data visualization
- **Animations**: AOS Animation Library, CSS animations

## Installation and Setup

### Prerequisites

- Python 3.8+ installed
- PostgreSQL (optional for production)
- Google Gemini API key
- Git (for cloning the repository)

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/essay-evaluation-platform.git
cd essay-evaluation-platform
```

### Step 2: Set Up Python Environment

```bash
# Create a virtual environment
python -m venv venv

# Activate virtual environment
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
# Install all required packages
pip install -r requirements.txt
```

Key packages in requirements.txt:
- flask
- flask-login
- flask-sqlalchemy
- flask-wtf
- google-generativeai
- gunicorn
- psycopg2-binary
- reportlab
- sqlalchemy
- werkzeug
- wtforms
- email-validator

### Step 4: Configure Environment Variables

Create a `.env` file in the project root with:

```
# Database Configuration
# For local development with SQLite:
DATABASE_URL=sqlite:///essay_evaluation.db

# For production with PostgreSQL:
# DATABASE_URL=postgresql://username:password@localhost:5432/essay_evaluation

# Google Gemini API key (REQUIRED)
GOOGLE_API_KEY=your_gemini_api_key

# Flask app secret key
SESSION_SECRET=your_secret_key_here
```

### Step 5: Initialize the Database

The application will automatically create the database tables when first started, but you can also do it manually:

```bash
# Start Python interpreter
python

# Create database tables
>>> from app import app, db
>>> with app.app_context():
>>>     db.create_all()
>>> exit()
```

### Step 6: Run the Application

```bash
# For development (using Flask's built-in server)
python main.py

# For production (using Gunicorn)
gunicorn --bind 0.0.0.0:5000 --workers=2 main:app
```

### Step 7: Access the Application

Open your web browser and navigate to:
- http://localhost:5000

## Running on Replit

If running this project on Replit:

1. The application is already configured to use PostgreSQL through the `DATABASE_URL` environment variable
2. Set the `GOOGLE_API_KEY` in the Secrets tab in your Replit project
3. The application will automatically start using the configured workflow

## Using the Application

### First Time Setup

1. Register two types of accounts:
   - Faculty account: For creating questions and evaluating submissions
   - Student account: For submitting answers to questions

2. As a faculty member:
   - Create essay questions with reference answers
   - Set word limits and maximum marks

3. As a student:
   - Browse available questions
   - Submit answers within the word limit

4. AI Evaluation Process:
   - Faculty members can trigger AI evaluation for all submissions
   - Each submission is evaluated on relevance, coverage, and structure
   - Scores and feedback are generated automatically

### Text Formatting Features

The application now properly supports multiline text with enhanced formatting:

- **Creating Questions**: Faculty can use multiple paragraphs and line breaks
- **Reference Answers**: Key answers maintain proper paragraph structure
- **Student Submissions**: Students can organize their answers with proper formatting
- **Evaluation Feedback**: AI feedback is displayed with proper paragraph breaks
- **PDF Reports**: All text formatting is preserved in generated PDF reports

Example of supported formatting:
```
Paragraph one with important information.

Paragraph two with:
- First point
- Second point
- Third point

Conclusion paragraph with summary.
```

## Google Gemini API Setup

This application requires a Google Gemini API key for the AI evaluation features:

1. Visit [Google AI Studio](https://ai.google.dev/)
2. Create a new API key in the API Keys section
3. Copy the key to your `.env` file as `GOOGLE_API_KEY=your_key_here`
4. The application uses the "gemini-1.5-pro" model for optimal evaluation

## Project Structure

```
essay-evaluation-platform/
├── app.py                  # Flask application setup and configuration
├── main.py                 # Application entry point
├── models.py               # Database models (User, Faculty, Student, Question, etc.)
├── forms.py                # Form definitions for all interfaces
├── routes/                 # Route handlers
│   ├── __init__.py         # Blueprint initialization
│   ├── auth.py             # Authentication routes (login, register, etc.)
│   ├── faculty.py          # Faculty-specific routes
│   └── student.py          # Student-specific routes
├── services/               # Business logic services
│   ├── __init__.py
│   ├── evaluation.py       # Gemini API integration for essay evaluation
│   └── pdf_generator.py    # PDF report generation with ReportLab
├── static/                 # Static assets
│   ├── assets/             # Images and SVGs
│   ├── css/                # Custom styling
│   └── js/                 # JavaScript for animations and charts
├── templates/              # Jinja2 HTML templates
│   ├── base.html           # Base template with common elements
│   ├── auth/               # Authentication templates
│   ├── faculty/            # Faculty interface templates
│   └── student/            # Student interface templates
├── requirements.txt        # Python dependencies
└── README.md               # Project documentation
```

## Troubleshooting

### Database Issues
- **SQLite Connection Error**: Check that the path to the SQLite file is correct and that the directory is writable
- **PostgreSQL Connection Error**: Verify your DATABASE_URL and ensure PostgreSQL is running

### API Integration Problems
- **Gemini API Error**: Ensure your GOOGLE_API_KEY is valid and has necessary permissions
- **"API Key not set" Error**: Check that the environment variable is correctly loaded
- **Response Format Error**: The application expects a specific format from the Gemini API; check for API changes

### Application Errors
- **Template Rendering Issues**: Check for missing variables in the route handlers
- **Form Validation Errors**: Ensure all form fields meet validation requirements
- **Authentication Problems**: Verify user roles and permissions in the database

## Performance and Scaling

- Each essay evaluation requires a call to the Gemini API, which may take 10-15 seconds
- For large classes, evaluate submissions in smaller batches
- The application works well for classes of up to 50-100 students
- For larger deployments, consider adding caching and optimizing database queries

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Credits

Developed for Jain University's academic evaluation system to streamline the essay assessment process.