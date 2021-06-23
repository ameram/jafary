from main import app, db, User, Counselor, Group, Subgroup, Request, Payment,  Respond, Type, State, Schedule

@app.shell_context_processor
def make_shell_context():
    return dict(app=app, db=db, User=User, Counselor=Counselor,
            Group=Group, Subgroup=Subgroup, Request=Request, Payment=Payment, Respond=Respond, Type=Type, State=State, Schedule=Schedule)
