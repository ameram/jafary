from flask import Flask, render_template, redirect, url_for, abort, flash, request, \
    current_app, make_response, Blueprint, session, g
from flask_login.utils import login_required
from flask_login import current_user
from sqlalchemy import func
# from sqlalchemy.sql.functions import current_user
from .models import db, Request, User, Counselor, Respond, Payment, Group, Subgroup, Role
from .forms import RequestForm, RespondForm, PaymentForm
from ..auth import has_role


qa_blueprint = Blueprint(
    'qa',
    __name__,
    template_folder='../templates/qa/',
    url_prefix="/qa"
)


def sidebar_data():
    recent = Request.query.filter_by(
        type_foreignkey='2').order_by(Request.pub_date.desc()).limit(5).all()

    return recent


@qa_blueprint.route('/')
@qa_blueprint.route('/<int:page>')
def home(page=1):
    requests = Request.query.order_by(Request.pub_date.desc()).paginate(
        page, current_app.config.get('POSTS_PER_PAGE', 10), False)
    recent = sidebar_data()

    return render_template('home.html', requests=requests, recent=recent)


@qa_blueprint.route('/group/<string:group_title>')
def requests_by_group(group_title):
    group = Group.query.filter_by(title=group_title).first_or_404()
    requests = group.requests.order_by(Request.pub_date.desc()).all()
    recent = sidebar_data()

    return render_template('group.html', requests=requests, group=group, recent=recent)


@qa_blueprint.route('/request/<int:request_id>', methods=('GET', 'POST'))
def request(request_id):
    request = Request.query.get_or_404(request_id)
    recent = sidebar_data()
    form = RespondForm()
    responds = request.responds.all()
    zz = list()
    for i in responds:
        zz.append((i, User.query.get(i.user_foreignkey)))
    if form.validate_on_submit() and current_user is not None:
        if current_user.roles.__contains__(Role.query.filter_by(name="counselor").first()):
            res = Respond()
            res.content = form.content.data
            res.user_foreignkey = current_user.id
            res.request_foreignkey = request.id
            db.session.add(res)
            db.session.commit()
            flash('Respond added.')
            return redirect(url_for('qa.request', request_id=res.id))
        else:
            flash('You should be counselor')
    return render_template('request.html', request=request, recent=recent, form=form, zz=zz)


@qa_blueprint.route('/user/<string:username>')
def requests_by_user(username):
    user = User.query.filter_by(username=username).first_or_404()
    requests = user.requests.order_by(
        Request.pub_date.desc()).all()
    recent = sidebar_data()
    return render_template('user.html', user=user, requests=requests, recent=recent)


@qa_blueprint.route('/create', methods=('GET', 'POST'))
@login_required
@has_role('user')
def create_request():
    form = RequestForm()
    if form.validate_on_submit():
        req = Request()
        req.title = form.title.data
        req.content = form.content.data
        req.user_foreignkey = current_user.id
        req.group_foreignkey = form.group.data
        req.subgroup_foreignkey = form.subgroup.data
        req.type_foreignkey = 1 if form.paid.data == True else 2
        db.session.add(req)
        db.session.commit()
        flash('Request added.')
        return redirect(url_for('qa.request', request_id=req.id))
    return render_template('create.html', form=form)


@qa_blueprint.route('/edit/<int:id>', methods=('GET', 'POST'))
@login_required
@has_role('user')
def edit_post(id):
    request = Request.query.get_or_404(id)
    if current_user.id == request.user_foreignkey:
        form = RequestForm()
        if form.validate_on_submit():
            request.title = form.title.data
            request.content = form.content.data
            request.group_foreignkey = form.group.data
            db.session.merge(request)
            db.session.commit()
            flash('Edited')
            print(f'\n\n{request.id}\n\n')
            return redirect(url_for('qa.request', request_id=request.id))
        form.title.data = request.title
        form.content.data = request.content
        form.group.data = request.group_foreignkey
        return render_template('edit.html', form=form, request=request)
    abort(403)


@qa_blueprint.route('/pay/<int:id>', methods=('GET', 'POST'))
@login_required
@has_role('counselor')
def pay_schdule(id):
    request = Request.query.get_or_404(id)
    if not current_user.id == request.user_foreignkey:
        form = PaymentForm()
        if form.validate_on_submit():
            payment = Payment()
            payment.value = float(form.value.data)
            payment.pay_date = form.date.data
            payment.method = form.method.data
            payment.counselor_foreignkey = current_user.id
            db.session.add(request)
            db.session.commit()
            request.payment_foreignkey = payment.id
            flash('Payment added')
            return redirect(url_for('qa.request', request_id=request.id))
        return render_template('payment.html', form=form, request=request)
    abort(403)

