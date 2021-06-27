import functools
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_login import AnonymousUserMixin, current_user
from flask import abort

login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.session_protection = "strong"
login_manager.login_message = "Please login to access this page"
login_manager.login_message_category = "info"

bcrypt = Bcrypt()


def has_role(name):
    def real_decorator(f):
        def wraps(*args, **kwargs):
            if current_user.has_role(name):
                return f(*args, **kwargs)
            else:
                abort(403)
        return functools.update_wrapper(wraps, f)
    return real_decorator


@login_manager.user_loader
def load_user(userid):
    from ..qa.models import User
    return User.query.get(userid)


def create_module(app, **kwargs):
    bcrypt.init_app(app)
    login_manager.init_app(app)
    from .controllers import auth_blueprint
    app.register_blueprint(auth_blueprint)


class BlogAnonymous(AnonymousUserMixin):

    def __init__(self):
        self.username = 'Guest'
