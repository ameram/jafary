from flask import Flask, render_template, redirect, url_for, abort, flash, request, \
    current_app, make_response, Blueprint, session, g
from flask_login.utils import login_required
from flask_login import current_user, AnonymousUserMixin, mixins
from sqlalchemy import func
from sqlalchemy.sql.functions import user
from .models import db, Request, User, Respond, Payment, Group, Subgroup, Role
from .forms import RequestForm, RespondForm, PaymentForm, GroupForm, SubgroupForm
from ..auth import has_role


qa_blueprint = Blueprint(
    'qa',
    __name__,
    template_folder='../templates/qa/',
    url_prefix="/qa"
)


def sidebar_data():
    recent = Request.query.filter_by(paid=False).order_by(
        Request.pub_date.desc()).limit(10).all()
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
    subgroups = group.subgroups.all()
    requests = group.requests.order_by(Request.pub_date.desc()).all()
    recent = sidebar_data()

    return render_template('group.html',
                           requests=requests,
                           group=group,
                           recent=recent,
                           subgroups=subgroups)


@qa_blueprint.route('/group/<int:group_id>')
def group_by_id(group_id):
    group = Group.query.get_or_404(group_id)
    subgroups = group.subgroups.all()
    requests = group.requests.order_by(Request.pub_date.desc()).all()
    recent = sidebar_data()

    return render_template('group.html',
                           requests=requests,
                           group=group,
                           recent=recent,
                           subgroups=subgroups)


@qa_blueprint.route('/request/<int:request_id>', methods=('GET', 'POST'))
def request(request_id):
    request = Request.query.get_or_404(request_id)
    recent = sidebar_data()
    form = RespondForm()
    responds = request.responds.all()
    zz = list()
    payments = list()
    for i in responds:
        zz.append((i, User.query.get(i.user_foreignkey)))

    if current_user.is_anonymous:
        pass
    elif current_user.id == request.user_foreignkey:
        payments = request.arrangements
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
    return render_template('request.html', request=request, recent=recent, form=form, zz=zz, payments=payments)


@qa_blueprint.route('/user/<string:username>')
def requests_by_user(username):
    user = User.query.filter_by(username=username).first_or_404()
    requests = user.requests.order_by(
        Request.pub_date.desc()).all()
    recent = sidebar_data()
    return render_template('user.html', user=user, requests=requests, recent=recent)


@qa_blueprint.route('/create', methods=('GET', 'POST'))
@login_required
@has_role('default')
def create_request():
    form = RequestForm()
    if form.validate_on_submit():
        req = Request()
        req.title = form.title.data
        req.content = form.content.data
        req.user_foreignkey = current_user.id
        req.group_foreignkey = form.group.data
        req.subgroup_foreignkey = form.subgroup.data
        req.paid = form.paid.data
        db.session.add(req)
        db.session.commit()
        flash(f'Request {req.id} added.')
        return redirect(url_for('qa.request', request_id=req.id))
    return render_template('create.html', form=form)


@qa_blueprint.route('/edit/<int:id>', methods=('GET', 'POST'))
@login_required
@has_role('default')
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


@qa_blueprint.route('/create_group/', methods=('GET', 'POST'))
@login_required
@has_role('admin')
def create_group():
    form = GroupForm()
    if form.validate_on_submit():
        group = Group()
        group.title = form.title.data
        db.session.add(group)
        db.session.commit()
        flash('Group added')
        return redirect(url_for('qa.requests_by_group', group_title=group.title))
    return render_template('greate.html', form=form)
    abort(403)


@qa_blueprint.route('/create_subgroup/', methods=('GET', 'POST'))
@login_required
@has_role('admin')
def create_sub():
    form = SubgroupForm()
    if form.validate_on_submit():
        subgroup = Subgroup()
        subgroup.title = form.title.data
        subgroup.group_foreignkey = form.group.data
        db.session.add(subgroup)
        db.session.commit()
        flash('Group added')
        return redirect(url_for('qa.group_by_id', group_id=form.group.data))
    return render_template('subgreate.html', form=form)
    abort(403)


@qa_blueprint.route('/usercontrol/', methods=('GET', 'POST'))
@login_required
@has_role('admin')
def user_controller():
    users = User.query.all()
    ucount = len(users)
    rcount = len(Request.query.all())
    gcount = len(Group.query.all())
    sgcount = len(Subgroup.query.all())
    defs = [i for i in users if not i.has_role("counselor")]
    return render_template('usercontrol.html',
                           defaults=defs,
                           count=ucount,
                           request_count=rcount,
                           group_count=gcount,
                           subgroup_count=sgcount)


@qa_blueprint.route('/verify/<int:user_id>', methods=('GET', 'POST'))
@login_required
@has_role('admin')
def user_verify(user_id):
    user = User.query.get(user_id)
    user.roles.append(Role.query.filter_by(name="counselor").first())
    db.session.merge(user)
    db.session.commit()
    return redirect(url_for('qa.home'))
