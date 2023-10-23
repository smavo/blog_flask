from flask import Blueprint, render_template, request, url_for, redirect, flash, session, g
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from core import db
from werkzeug.utils import secure_filename
import os

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if g.user:
        flash("No puedes acceder al registro, ya que estas logeado", 'warning')
        return redirect(url_for('post.posts'))

    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        user = User(username, email, generate_password_hash(password))

        # Validación de datos
        error = None

        # Comparando nombre de usuario con los existentes
        user_email = User.query.filter_by(email=email).first()
        if user_email == None:
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('auth.login'))
        else:
            error = f'El correo {email} ya esta registrado'

        flash(error)

    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if g.user:
        flash("No puedes acceder al login, ya que estas logeado", 'warning')
        return redirect(url_for('post.posts'))

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Validando datos
        error = None
        user = User.query.filter_by(email=email).first()

        if user == None or not check_password_hash(user.password, password):
            error = 'Correo o contraseña incorrecta'

        # Iniciando sessión
        if error is None:
            session.clear()
            session['user_id'] = user.id
            flash("Inicio de sessión éxito", 'success')
            return redirect(url_for('post.posts'))

        flash(error, 'error')

    return render_template('auth/login.html')


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = User.query.get_or_404(user_id)


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home.index'))


import functools


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            flash('Debes iniciar sesión para acceder', 'warning')
            return redirect(url_for('auth.login'))
        return view(**kwargs)

    return wrapped_view


@bp.route('/profile/<int:id>', methods=('GET', 'POST'))
@login_required
def profile(id):
    user = User.query.get_or_404(id)

    if request.method == 'POST':
        user.username = request.form.get('username')
        user.email = request.form.get('email')
        password = request.form.get('password')

        error = None

        if len(password) != 0:
            user.password = generate_password_hash(password)
        elif len(password) > 0 and len(password) < 6:
            error = 'La contraseña debe tener mas 5 caracteres'

        if 'photo' in request.files:
            photo = request.files['photo']
            if photo.filename != '':
                if user.photo:
                    # Eliminar la imagen anterior si existe
                    try:
                        os.remove(f'core/static/{user.photo}')
                    except OSError as e:
                        flash(f"Error al eliminar la imagen anterior: {e}")

                # Guardar la nueva imagen
                filename = secure_filename(photo.filename)
                photo.save(f'core/static/media/{filename}')
                user.photo = f'media/{filename}'

        if error is not None:
            flash(error)
        else:
            db.session.commit()
            flash("Perfil actualizado con éxito", 'success')
            return redirect(url_for('auth.profile', id=user.id))

        flash(error)

    return render_template('auth/profile.html', user=user)

