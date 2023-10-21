from flask import Blueprint, render_template, request

bp = Blueprint('home', __name__)


@bp.route('/')
def index():
    return render_template('index.html')


@bp.route('/blog')
def blog():
    return 'Pagina del Blog'
