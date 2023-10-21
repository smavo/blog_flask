from flask import Blueprint, render_template, request

bp = Blueprint('home', __name__)


@bp.route('/')
def index():
    return 'Pagina de Inicio'


@bp.route('/blog')
def blog():
    return 'Pagina del Blog'
