from flask import Blueprint, render_template, request

bp = Blueprint('post', __name__, url_prefix = '/post')


@bp.route('/posts')
def posts():
    return 'Pagina de todos los posts'


@bp.route('/create')
def create():
    return 'Crear Post'


@bp.route('/update')
def update():
    return 'Actualizar Post'


@bp.route('/delete')
def delete():
    return 'Eliminar Post'

