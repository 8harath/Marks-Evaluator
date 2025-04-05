from datetime import datetime
from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(10), nullable=False)  # 'faculty' or 'student'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    __mapper_args__ = {
        'polymorphic_on': role,
        'polymorphic_identity': 'user'
    }
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>'

class Faculty(User):
    __tablename__ = 'faculty'
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    department = db.Column(db.String(100))
    questions = db.relationship('Question', backref='faculty', lazy='dynamic')
    
    __mapper_args__ = {
        'polymorphic_identity': 'faculty'
    }

class Student(User):
    __tablename__ = 'student'
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    submissions = db.relationship('Submission', backref='student', lazy='dynamic')
    
    __mapper_args__ = {
        'polymorphic_identity': 'student'
    }

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    key_answer = db.Column(db.Text, nullable=False)
    word_limit = db.Column(db.Integer, nullable=False)
    max_marks = db.Column(db.Integer, nullable=False)
    faculty_id = db.Column(db.Integer, db.ForeignKey('faculty.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    submissions = db.relationship('Submission', backref='question', lazy='dynamic')
    
    def __repr__(self):
        return f'<Question {self.id}>'

class Submission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    answer_text = db.Column(db.Text, nullable=False)
    word_count = db.Column(db.Integer, nullable=False)
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)
    evaluation = db.relationship('Evaluation', backref='submission', uselist=False, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Submission {self.id}>'

class Evaluation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    relevance_score = db.Column(db.Float, nullable=False)
    coverage_score = db.Column(db.Float, nullable=False)
    structure_score = db.Column(db.Float, nullable=False)
    total_score = db.Column(db.Float, nullable=False)
    rank = db.Column(db.Integer, nullable=True)
    feedback = db.Column(db.Text, nullable=True)
    evaluated_at = db.Column(db.DateTime, default=datetime.utcnow)
    submission_id = db.Column(db.Integer, db.ForeignKey('submission.id'), nullable=False, unique=True)
    
    def __repr__(self):
        return f'<Evaluation {self.id}>'
