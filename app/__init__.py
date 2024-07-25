from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

# Инициализация Flask приложения
app = Flask(__name__)
# Установка секретного ключа для сессий
app.config['SECRET_KEY'] = 'your_secret_key'
# Настройка базы данных
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

# Инициализация расширений Flask
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'  # Установка представления для страницы входа

from app import routes  # Импорт маршрутов
