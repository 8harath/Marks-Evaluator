from flask import Blueprint, render_template, url_for, flash, redirect, request
from flask_login import login_user, current_user, logout_user, login_required
from app import db
from models import User, Faculty, Student
from forms import LoginForm, RegistrationForm, FacultyProfileForm

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/')
def index():
    return render_template('index.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        if current_user.role == 'faculty':
            return redirect(url_for('faculty.dashboard'))
        else:
            return redirect(url_for('student.dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            
            if user.role == 'faculty':
                return redirect(next_page) if next_page else redirect(url_for('faculty.dashboard'))
            else:
                return redirect(next_page) if next_page else redirect(url_for('student.dashboard'))
        else:
            flash('Login unsuccessful. Please check email and password.', 'danger')
    
    return render_template('auth/login.html', title='Login', form=form)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        if form.role.data == 'faculty':
            user = Faculty(username=form.username.data, email=form.email.data)
        else:
            user = Student(username=form.username.data, email=form.email.data)
        
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        
        flash(f'Account created for {form.username.data}! You can now log in.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html', title='Register', form=form)

@auth_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.index'))

@auth_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if current_user.role == 'faculty':
        form = FacultyProfileForm()
        if form.validate_on_submit():
            current_user.department = form.department.data
            db.session.commit()
            flash('Your profile has been updated!', 'success')
            return redirect(url_for('auth.profile'))
        elif request.method == 'GET':
            form.department.data = current_user.department
        
        return render_template('auth/profile.html', title='Profile', form=form)
    else:
        # For student profile (can be expanded later)
        return render_template('auth/profile.html', title='Profile')
