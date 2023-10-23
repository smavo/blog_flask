from flask import Blueprint, render_template, request, session
from .auth import login_required
from .models import Post
from core import db

bp = Blueprint('post', __name__, url_prefix='/post')


@bp.route('/posts')
@login_required
def posts():
    user_id = session.get('user_id')
    posts = Post.query.filter_by(author=user_id).all()
    # posts = Post.query.all()
    return render_template('admin/posts.html', posts=posts)


@bp.route('/create')
def create():
    return 'Crear Post'


@bp.route('/update')
def update():
    return 'Actualizar Post'


@bp.route('/delete')
def delete():
    return 'Eliminar Post'
