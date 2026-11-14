from datetime import datetime

from . import db


class Opinion(db.Model):
    """Модель мнения о фильме.

    Хранит название фильма, текст мнения, ссылку на источник,
    временную метку создания и автора (опционально).
    """
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    text = db.Column(db.Text, unique=True, nullable=False)
    source = db.Column(db.String(256))
    timestamp = db.Column(
        db.DateTime,
        index=True,
        default=datetime.utcnow
    )
    added_by = db.Column(db.String(64))
