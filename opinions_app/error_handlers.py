from flask import render_template

from . import db


def page_not_found(error):
    """Обработчик ошибки 404: страница не найдена."""
    return render_template('404.html'), 404


def internal_error(error):
    """Обработчик ошибки 500: внутренняя ошибка сервера.

    Откатывает текущую транзакцию сессии, чтобы избежать
    неконсистентного состояния базы данных.
    """
    db.session.rollback()
    return render_template('500.html'), 500
