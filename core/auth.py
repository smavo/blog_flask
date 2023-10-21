from flask import Blueprint, render_template, request

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register')
def register():
    return 'Pagina de Registro de Usuario'


@bp.route('/login')
def login():
    return 'Pagina de Login del Blog'


@bp.route('/profile')
def profile():
    return 'Pagina de Perfil de Usuario'
