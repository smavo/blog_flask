from flask import Flask


def create_app():
    # Crear aplicación de flask
    app = Flask(__name__)

    app.config.from_object('config.Config')

    # Registrar vistas
    from core import home
    app.register_blueprint(home.bp)

    from core import auth
    app.register_blueprint(auth.bp)

    from core import posts
    app.register_blueprint(posts.bp)

    return app

