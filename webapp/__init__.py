from flask import Flask, app, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import MetaData



convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}


metadata = MetaData(naming_convention=convention)
db = SQLAlchemy(metadata=metadata)
# db = SQLAlchemy()
migrate = Migrate()


def page_not_found(error):
    return render_template('404.html'), 404


def create_app(object_name):
    from .qa.controllers import qa_blueprint
    from .main.controllers import main_blueprint
    from .auth import create_module as auth_create_module

    app = Flask(__name__)
    app.config.from_object(object_name)

    metadata = MetaData(naming_convention=convention)
    db.init_app(app)
    migrate.init_app(app, db, render_as_batch=True)
    app.register_blueprint(main_blueprint)
    app.register_blueprint(qa_blueprint)
    app.register_error_handler(404, page_not_found)
    auth_create_module(app)
    return app
