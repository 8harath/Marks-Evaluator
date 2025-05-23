import os
import logging
from datetime import datetime

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from werkzeug.middleware.proxy_fix import ProxyFix
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect

# Configure logging
logging.basicConfig(level=logging.DEBUG)

class Base(DeclarativeBase):
    pass

# Initialize extensions
db = SQLAlchemy(model_class=Base)
login_manager = LoginManager()
csrf = CSRFProtect()

# Create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Configure the database
db_url = os.environ.get("DATABASE_URL", "sqlite:///essay_evaluation.db")

# Handle SQLite URL (SQLAlchemy 1.4+ compatibility)
if db_url.startswith("sqlite"):
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url
    # SQLite specific configurations
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
        "connect_args": {"check_same_thread": False}
    }
else:
    # PostgreSQL configuration
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
        "pool_recycle": 300,
        "pool_pre_ping": True,
    }
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize the extensions with the app
db.init_app(app)
login_manager.init_app(app)
csrf.init_app(app)
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'

# Add context processor to provide current date to all templates
@app.context_processor
def inject_now():
    return {'now': datetime.now()}

# Add custom Jinja2 filters
@app.template_filter('nl2br')
def nl2br(value):
    """Convert newlines to <br> tags."""
    if value:
        return value.replace('\n', '<br>\n')
    return ''

with app.app_context():
    # Import models
    from models import User, Faculty, Student, Question, Submission, Evaluation
    
    # Import routes
    from routes.auth import auth_bp
    from routes.faculty import faculty_bp
    from routes.student import student_bp
    
    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(faculty_bp)
    app.register_blueprint(student_bp)
    
    # Create database tables
    db.create_all()
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
        
    @app.route('/ping')
    def ping():
        return 'pong'
