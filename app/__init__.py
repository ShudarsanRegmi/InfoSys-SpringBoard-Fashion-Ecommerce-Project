from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from .models import db, User
from itsdangerous import URLSafeTimedSerializer
from flask_migrate import Migrate
from .views import bp
login_manager = LoginManager()
URL_SERIALIZER = None


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def create_app(config=None):
    app = Flask(__name__)
    if config:
        app.config.update(config)
    app.secret_key = "Infosys-Springboard-5.0"
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # app = Flask(__name__, static_folder='app/static')
    migrate = Migrate(app, db)
    global URL_SERIALIZER
    URL_SERIALIZER = URLSafeTimedSerializer(app.config['SECRET_KEY'])
 
    # Initialize extensions with app
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    #for solving circular import problem
    from . import views, auth, admin
    app.register_blueprint(auth.bp)
    app.register_blueprint(views.bp)
    app.register_blueprint(admin.admin, url_prefix='/admin')

    # Create tables
    with app.app_context():
        db.create_all()

    return app


