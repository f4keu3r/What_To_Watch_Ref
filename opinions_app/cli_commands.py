import csv

import click
from flask.cli import with_appcontext

from . import db
from .models import Opinion


@click.command('load_opinions')
@with_appcontext
def load_opinions_command():
    """CLI-команда для загрузки мнений из CSV-файла в базу данных.

    Ожидает файл opinions.csv в текущей директории с колонками,
    соответствующими полям модели Opinion.
    """
    with open('opinions.csv', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        counter = 0
        for row in reader:
            opinion = Opinion(**row)
            db.session.add(opinion)
            # TODO: коммитить пакетно, а не после каждой записи,
            # чтобы не делать лишних запросов к БД
            db.session.commit()
            counter += 1
    click.echo(f'Загружено мнений: {counter}')
