from main import app, db, User, Counselor, Group, Subgroup


@app.shell_context_processor
def make_shell_context():
    return dict(app=app, db=db, User=User, Counselor=Counselor, Group=Group, Subgroup=Subgroup)
