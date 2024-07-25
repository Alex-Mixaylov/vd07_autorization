from flask import render_template, request, redirect, url_for, flash, session
from flask_login import login_user, logout_user, current_user, login_required
from app.models import User
from app import app, db, bcrypt
from app.forms import RegistrationForm, LoginForm, UpdateAccountForm
import random

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Вы успешно зарегистрировались!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form, title='Register')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('home'))
        else:
            flash('Введены неверные данные')
    return render_template('login.html', form=form, title='Login')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    if 'captcha_num1' not in session or 'captcha_num2' not in session:
        session['captcha_num1'] = random.randint(1, 10)
        session['captcha_num2'] = random.randint(1, 10)
    form = UpdateAccountForm(current_user=current_user)
    if form.validate_on_submit():
        if bcrypt.check_password_hash(current_user.password, form.old_password.data):
            if form.captcha.data != str(session['captcha_num1'] + session['captcha_num2']):
                flash('Неправильный ответ на капчу', 'danger')
            else:
                current_user.username = form.username.data
                current_user.email = form.email.data
                if form.new_password.data:
                    hashed_password = bcrypt.generate_password_hash(form.new_password.data).decode('utf-8')
                    current_user.password = hashed_password
                db.session.commit()
                flash('Ваш аккаунт был обновлен!', 'success')
                session.pop('captcha_num1', None)
                session.pop('captcha_num2', None)
                return redirect(url_for('account'))
        else:
            flash('Неверный старый пароль', 'danger')
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template('account.html', form=form, title='Account', captcha_num1=session['captcha_num1'], captcha_num2=session['captcha_num2'])
