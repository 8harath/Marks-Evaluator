from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, IntegerField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError, NumberRange
from models import User

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    role = StringField('Role', validators=[DataRequired()])
    submit = SubmitField('Sign Up')
    
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is already taken. Please choose a different one.')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is already registered. Please use a different one.')

class FacultyProfileForm(FlaskForm):
    department = StringField('Department', validators=[DataRequired()])
    submit = SubmitField('Update Profile')

class QuestionForm(FlaskForm):
    text = TextAreaField('Question Text', validators=[DataRequired()])
    key_answer = TextAreaField('Key Answer (Reference Solution)', validators=[DataRequired()])
    word_limit = IntegerField('Word Limit', validators=[DataRequired(), NumberRange(min=50, max=2000)])
    max_marks = IntegerField('Maximum Marks', validators=[DataRequired(), NumberRange(min=10, max=100)])
    submit = SubmitField('Create Question')

class SubmissionForm(FlaskForm):
    answer_text = TextAreaField('Your Answer', validators=[DataRequired()])
    submit = SubmitField('Submit Answer')
    
    def validate_answer_text(self, answer_text):
        # Word count validation will be handled client-side with JavaScript
        # This is a fallback server-side validation
        word_count = len(answer_text.data.split())
        if word_count < 10:  # Minimum sensible word count
            raise ValidationError('Your answer is too short. Please elaborate more.')

class SimpleStudentForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Continue to Answer')
