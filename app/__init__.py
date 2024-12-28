from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    
    # Configurations
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = 'Infosys-Springboard-5.0'
    
    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    
    # Register Blueprints
    from .views import views
    app.register_blueprint(views)
    
    with app.app_context():
        db.create_all()
    
    return app
