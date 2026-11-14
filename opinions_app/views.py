from random import randrange

from flask import abort, flash, redirect, render_template, url_for

from . import db
from .forms import OpinionForm
from .models import Opinion


def index_view():
    """Главная страница: показывает случайное мнение о фильме.

    Если в базе нет ни одного мнения, возвращает ошибку 500.
    """
    quantity = Opinion.query.count()
    if not quantity:
        # Нет смысла выбирать случайную запись из пустой таблицы
        abort(500)
    # randrange(quantity) возвращает число от 0 до quantity - 1
    offset_value = randrange(quantity)
    opinion = Opinion.query.offset(offset_value).first()
    return render_template('opinion.html', opinion=opinion)


def add_opinion_view():
    """Добавляет новое мнение о фильме.

    При GET-запросе отображает пустую форму, при POST — валидирует
    и сохраняет мнение. Дубликаты по тексту не допускаются.
    """
    form = OpinionForm()
    if form.validate_on_submit():
        text = form.text.data
        # Проверка на дубликат: поле text в модели unique=True
        if Opinion.query.filter_by(text=text).first() is not None:
            flash('Такое мнение уже было оставлено ранее!')
            return render_template('add_opinion.html', form=form)
        opinion = Opinion(
            title=form.title.data,
            text=text,
            source=form.source.data
        )
        db.session.add(opinion)
        db.session.commit()
        return redirect(url_for('opinion_view', id=opinion.id))
    return render_template('add_opinion.html', form=form)


def opinion_view(id):
    """Отображает мнение о фильме по его идентификатору.

    Если мнение не найдено, возвращает 404.
    """
    opinion = Opinion.query.get_or_404(id)
    return render_template('opinion.html', opinion=opinion)
