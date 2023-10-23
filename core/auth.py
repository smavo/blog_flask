from flask import Blueprint, render_template, request, url_for, redirect, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from core import db

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods = ('GET', 'POST'))
def register():
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
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Validando datos
        error = None
        user = User.query.filter_by(email=email).first()

        if user == None or not check_password_hash(user.password, password):
            error = 'Correo o contraseña incorrecta'

        # Iniciando sesion
        if error is None:
            session.clear()
            session['user_id'] = user.id
            return redirect(url_for('post.posts'))

        flash(error)

    return render_template('auth/login.html')


@bp.route('/profile')
def profile():
    return 'Pagina de Perfil de Usuario'
