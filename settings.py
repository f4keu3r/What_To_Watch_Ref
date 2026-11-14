import os

from dotenv import load_dotenv

# Загружаем переменные из .env в окружение процесса.
# По умолчанию ищет .env в текущей рабочей директории.
load_dotenv()


class Config(object):
    """Конфигурация Flask-приложения.

    Реальные значения берутся из переменных окружения (.env),
    в коде остаются только имена настроек и безопасные дефолты.
    """
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'SQLALCHEMY_DATABASE_URI',
        'sqlite:///db.sqlite3'
    )
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
