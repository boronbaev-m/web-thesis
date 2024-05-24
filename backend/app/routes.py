from flask import render_template, url_for, flash, redirect, request, Blueprint, jsonify
from flask_login import login_user, current_user, logout_user, login_required
from app import db, bcrypt, queue
from app.models import User, Code
from app.utils import check_code
from app.forms import RegistrationForm, LoginForm, CodeForm
import torch
from transformers import RobertaTokenizer, AutoModelForSequenceClassification
from app.models import Code
from app import db
from .utils import check_code_raw

main = Blueprint('main', __name__)
users = Blueprint('users', __name__)
code = Blueprint('code', __name__)

@main.route('/')
@main.route('/home')
def home():
    return render_template('index.html')

@main.route('/result')
def result():
    return render_template('result.html')

@users.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form)

@users.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.home'))

@code.route('/submit', methods=['POST'])
# @login_required
def submit():
    data = request.get_json()
    code_content = data.get('code')
    res = check_code_raw(code_content)
    return jsonify({'result': res}), 202

@code.route('/result/<job_id>', methods=['GET'])
# @login_required
def get_result(job_id):
    job = queue.fetch_job(job_id)
    if job.is_finished:
        code_entry = Code.query.get(job.result)
        return jsonify({'result': code_entry.result})
    else:
        return jsonify({'status': job.get_status()}), 202
