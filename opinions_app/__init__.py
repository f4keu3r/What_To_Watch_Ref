from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from settings import Config

# Расширения без привязки к приложению
db = SQLAlchemy()
migrate = Migrate()

# Единственный экземпляр приложения
app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
migrate.init_app(app, db)


def create_app(config_object=Config):
    app = Flask(__name__)
    app.config.from_object(config_object)

    db.init_app(app)
    migrate.init_app(app, db)

    from .views import index_view, add_opinion_view, opinion_view
    from .error_handlers import page_not_found, internal_error
    from .cli_commands import load_opinions_command

    app.add_url_rule('/', view_func=index_view)
    app.add_url_rule(
        '/add', view_func=add_opinion_view, methods=['GET', 'POST']
    )
    app.add_url_rule('/opinion/<int:id>', view_func=opinion_view)
    app.register_error_handler(404, page_not_found)
    app.register_error_handler(500, internal_error)
    app.cli.add_command(load_opinions_command)

    return app


app = create_app()
# Импорт модулей регистрирует views, обработчики ошибок и CLI-команды.
# Важно: импорт идёт ПОСЛЕ создания app и db, иначе circular import.
from . import views, error_handlers, cli_commands  # noqa: E402,F401
