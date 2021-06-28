import os
from webapp import db, migrate, create_app
from webapp.qa.models import User, Counselor, Group, Subgroup, Request, Payment,  Respond, Type, State


env = os.environ.get('WEBAPP_ENV', 'dev')
app = create_app(f'config.{env.capitalize()}Config')


@app.shell_context_processor
def make_shell_context():
    return dict(app=app, db=db, User=User, Counselor=Counselor,
                Group=Group, Subgroup=Subgroup, Request=Request, Payment=Payment, Respond=Respond, Type=Type, State=State, migrate=migrate)
