from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.models import User
import random

class RegistrationForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired(), Length(min=2, max=35)])
    email = StringField('Электронная почта', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    confirm_password = PasswordField('Подтверждение пароля', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Зарегистрироваться')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Такое имя уже существует')

    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError('Такая почта уже используется')

class LoginForm(FlaskForm):
    email = StringField('Электронная почта', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember = BooleanField('Запомни меня')
    submit = SubmitField('Войти')

class UpdateAccountForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired(), Length(min=2, max=35)])
    email = StringField('Электронная почта', validators=[DataRequired(), Email()])
    old_password = PasswordField('Старый пароль', validators=[DataRequired()])
    new_password = PasswordField('Новый пароль', validators=[Length(min=6)])
    confirm_new_password = PasswordField('Подтверждение нового пароля', validators=[EqualTo('new_password')])
    captcha = StringField(validators=[DataRequired()])
    submit = SubmitField('Обновить')

    def __init__(self, current_user, *args, **kwargs):
        super(UpdateAccountForm, self).__init__(*args, **kwargs)
        self.current_user = current_user

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user and user != self.current_user:
            raise ValidationError('Такое имя уже существует')

    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email and email != self.current_user:
            raise ValidationError('Такая почта уже используется')
