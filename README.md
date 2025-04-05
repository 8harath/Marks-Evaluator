# Academic Essay Evaluation Platform

A Flask-based web application for automated evaluation of student essays using Google's Gemini AI. This platform provides tools for faculty to create essay questions and automatically evaluate student submissions across multiple dimensions.

![Essay Evaluation Platform](static/assets/jain_university_logo.svg)

## Features

- **User Authentication System**: Secure login and registration with role-based access (faculty/student)
- **Faculty Dashboard**: Create questions, view submissions, evaluate essays, generate PDF reports
- **Student Interface**: Browse available questions, submit answers, view feedback and scores
- **AI Evaluation**: Automated essay evaluation using Google's Gemini API
- **Interactive UI**: Smooth animations, dynamic charts, and responsive design
- **Data Visualization**: Score distribution, performance comparison, and detailed feedback

## Technology Stack

- **Backend**: Python 3, Flask framework
- **Database**: PostgreSQL (production) / SQLite (development)
- **ORM**: SQLAlchemy
- **Authentication**: Flask-Login
- **Forms**: Flask-WTF, WTForms
- **AI Integration**: Google Generative AI (Gemini API)
- **PDF Generation**: ReportLab
- **Frontend**: HTML, CSS, JavaScript
- **UI Framework**: Bootstrap 5
- **Charts**: Chart.js
- **Animations**: AOS Animation Library, Animate.css

## Installation Requirements

- Python 3.8+
- PostgreSQL (optional for production)
- Google Gemini API key

## Local Setup Instructions

1. **Clone the repository**

   ```bash
   git clone https://github.com/yourusername/essay-evaluation-platform.git
   cd essay-evaluation-platform
   ```

2. **Create and activate a virtual environment**

   ```bash
   # On Windows
   python -m venv venv
   venv\Scripts\activate

   # On macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**

   Create a `.env` file in the root directory with the following variables:

   ```
   DATABASE_URL=sqlite:///essay_evaluation.db
   GOOGLE_API_KEY=your_gemini_api_key
   SESSION_SECRET=your_secret_key
   ```

   For PostgreSQL (optional):
   ```
   DATABASE_URL=postgresql://username:password@localhost:5432/essay_evaluation
   ```

5. **Initialize the database**

   ```bash
   # Make sure you're in the project root directory
   python
   >>> from app import app, db
   >>> with app.app_context():
   >>>     db.create_all()
   >>> exit()
   ```

6. **Run the application**

   ```bash
   # Development mode
   python main.py

   # Or using Gunicorn (production)
   gunicorn --bind 0.0.0.0:5000 main:app
   ```

7. **Access the application**

   Open your web browser and navigate to: `http://localhost:5000`

## Getting a Google Gemini API Key

To use the AI evaluation features, you need a Google Gemini API key:

1. Visit [Google AI Studio](https://ai.google.dev/)
2. Sign in with your Google account
3. Navigate to the API keys section
4. Create a new API key
5. Add the key to your `.env` file as `GOOGLE_API_KEY`

## User Guide

### Faculty User

1. **Register** as a faculty member
2. **Create Questions** with reference answers and evaluation criteria
3. **View Submissions** from students
4. **Evaluate** student answers automatically using Gemini AI
5. **Review Results** with detailed analytics
6. **Generate PDF Reports** for documentation

### Student User

1. **Register** as a student
2. **Browse Questions** available for submission
3. **Submit Answers** with word count tracking
4. **View Feedback** on evaluated submissions
5. **Compare Performance** against class averages

## File Structure

```
essay-evaluation-platform/
├── app.py                  # Flask application configuration
├── main.py                 # Application entry point
├── models.py               # SQLAlchemy database models
├── forms.py                # WTForms form classes
├── routes/                 # Application routes
│   ├── __init__.py
│   ├── auth.py             # Authentication routes
│   ├── faculty.py          # Faculty-specific routes
│   └── student.py          # Student-specific routes
├── services/               # Business logic
│   ├── __init__.py
│   ├── evaluation.py       # Essay evaluation with Gemini API
│   └── pdf_generator.py    # PDF report generation
├── static/                 # Static assets
│   ├── assets/             # Images and SVGs
│   ├── css/                # Custom CSS
│   └── js/                 # JavaScript files
├── templates/              # Jinja2 templates
│   ├── base.html           # Base template
│   ├── index.html          # Homepage
│   ├── auth/               # Authentication templates
│   ├── faculty/            # Faculty interface templates
│   └── student/            # Student interface templates
└── requirements.txt        # Python dependencies
```

## Development Notes

- The application can work with both SQLite (for development) and PostgreSQL (for production)
- The default port is 5000, but can be changed in `main.py`
- For production deployment, use a proper WSGI server like Gunicorn

## Troubleshooting

- **Database Connection Issues**: Check your DATABASE_URL environment variable
- **API Key Errors**: Verify your GOOGLE_API_KEY is correctly set
- **Dependencies**: Ensure all requirements are installed
- **Port Conflicts**: Change the port in `main.py` if port 5000 is in use

## Performance Considerations

- The API evaluation can take 10-15 seconds per submission
- For large class sizes, batch evaluations in smaller groups
- Consider periodic database backups for production use

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Credits

Developed for Jain University's academic evaluation system.