from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_login import AnonymousUserMixin

login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.session_protection = "strong"
login_manager.login_message = "Please login to access this page"
login_manager.login_message_category = "info"

bcrypt = Bcrypt()

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
