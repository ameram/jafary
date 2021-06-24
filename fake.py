from random import randint
from . import db
from .main import Request
from sqlalchemy.exc import IntegrityError
dict = ['Anxiety disorder', 'Eating disorder', 'Sleep disorder']
desc = ['Anxiety disorder: Anxiety or fear that interferes with normal functioning may be classified as an anxiety disorder.',
        'These disorders involve disproportionate concern in matters of food and weight.',
        'These conditions are associated with disruption to normal sleep patterns. A common sleep disorder is insomnia, which is described as difficulty falling and/or staying asleep.']

def users(count=len(dict)):
    i = 0
    while i < count:
        r = Request(dict[i])
        r.content = desc[i]
        r.user_foreignkey = randint(0, 1)
        db.session.add(r)
        try:
            db.session.commit()
            i += 1
        except IntegrityError:
            db.session.rollback()

