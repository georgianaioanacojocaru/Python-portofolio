from flask import Flask
from .routes import routes
from .admin import admin
from .const import db


def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = "123456789"
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"

    app.register_blueprint(routes)
    app.register_blueprint(admin)

    db.init_app(app)
    with app.app_context():
        import webapp.models
        db.create_all()

    return app