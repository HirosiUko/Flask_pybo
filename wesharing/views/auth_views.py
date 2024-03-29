from flask import Blueprint, url_for, render_template, flash, request, session, g, jsonify
from werkzeug.security import generate_password_hash,check_password_hash
from werkzeug.utils import redirect
from datetime import datetime
import functools
import json

from wesharing import db
from wesharing.forms import UserCreateForm, UserLoginForm
from wesharing.models import User

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/signup/', methods=('GET', 'POST'))
def signup():
    form = UserCreateForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if not user:
            user = User(username=form.username.data,
                        password=generate_password_hash(form.password1.data),
                        email=form.email.data,
                        create_date=datetime.now(),
                        usernick=form.usernick.data,
                        userprofile=form.userprofile.data
                        )
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('main.index'))
        else:
            flash('이미 존재하는 사용자입니다.')
    return render_template('auth/signup.html', form=form)

@bp.route('/api_login/', methods=['POST'])
def api_login():
    print("들어오니")
    user = User.query.filter_by(username=request.form['username'].strip()).first()
    error = None
    if not user:
        error = '존재하지 않는 사용자입니다.'
        print(error)
    elif not check_password_hash(user.password, request.form['password'].strip()):
        error = "비밀번호가 올바르지 않습니다."
        print(error)
    if error is None:
        person_dic = [
            {
                "result" : "success"
        },
            {
            "user" : user.username,
            "email": user.email,
            "nick" : user.usernick,
            "create_date" : user.create_date.strftime("%Y/%m/%d, %H:%M:%S"),
            "userprofile" : user.userprofile,
            "pic" : "None"
        }]
        return jsonify(person_dic)
    return jsonify([{
        "result" : "failure"
    },
        {
            "reson": error
        }])


@bp.route('/login/', methods=('GET', 'POST'))
def login():
    form = UserLoginForm()
    print(form.csrf_token)
    if request.method == 'POST' and form.validate_on_submit():
        error = None
        user = User.query.filter_by(username=form.username.data).first()
        if not user:
            error = "존재하지 않는 사용자입니다."
        elif not check_password_hash(user.password, form.password.data):
            error = "비밀번호가 올바르지 않습니다."
        if error is None:
            session.clear()
            session['user_id'] = user.id
            _next = request.args.get('next', '')
            if _next:
                return redirect(_next)
            else:
                return redirect(url_for('main.index'))
        flash(error)
    return render_template('auth/login.html', form=form)

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = User.query.get(user_id)

@bp.route('/logout/')
def logout():
    session.clear()
    return redirect(url_for('main.index'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(*args, **kwargs):
        if g.user is None:
            _next = request.url if request.method == 'GET' else ''
            return redirect(url_for('auth.login', next=_next))
        return view(*args, **kwargs)
    return wrapped_view