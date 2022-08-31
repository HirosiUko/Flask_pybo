from flask import Blueprint, url_for
# from wesharing.models import Question
from werkzeug.utils import redirect

bp = Blueprint('main', __name__, url_prefix='/')

@bp.route('/hello')
def hello_We():
    return 'hello, wesharing!'

@bp.route('/')
def index():
    return redirect(url_for('question._list'))
