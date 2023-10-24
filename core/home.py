from flask import Blueprint, render_template, request
from .models import User, Post
from flask_paginate import Pagination, get_page_parameter

bp = Blueprint('home', __name__)


def get_user(id):
    user = User.query.get_or_404(id)
    return user


def search_posts(query):
    posts = Post.query.filter(Post.title.ilike(f'%{query}%')).all()
    return posts


@bp.route('/busqueda', methods=['GET'])
def search():
    query = request.args.get('search')
    if query:
        posts = search_posts(query)
        value = 'hidden'
    else:
        posts = []
        value = 'visible'
    return render_template('search.html', posts=posts, get_user=get_user, value=value)


@bp.route('/', methods=['GET', 'POST'])
def index():
    # posts = Post.query.all()
    posts = Post.query.order_by(Post.created.desc()).limit(4)  # Los últimos 5 Mostrar
    return render_template('index.html', posts=posts, get_user=get_user)


@bp.route('/blog/<url>')
def blog(url):
    post = Post.query.filter_by(url=url).first()
    return render_template('blog.html', post=post, get_user=get_user)


@bp.route('/posts')
def posts_index():
    # posts = Post.query.order_by(Post.created.asc()).all()
    # return render_template('posts.html', posts=posts, get_user=get_user)
    page = request.args.get('page', 1, type=int)
    per_page = 3
    posts = Post.query.paginate(page=page, per_page=per_page, error_out=False)
    return render_template('posts.html', posts=posts, get_user=get_user)


