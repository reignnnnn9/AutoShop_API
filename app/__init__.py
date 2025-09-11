from flask import Flask
from .models import db
from .extensions import ma
from .blueprints.customers import customer_bp

def create_app(config_name):

    app = Flask(__name__)
    app.config.from_object(f'config.{config_name}')

    # Initialize extensions - plugging them in 
    db.init_app(app)
    ma.init_app(app)

    # Register Blueprints
    app.register_blueprint(customer_bp, url_prefix='/customers')
    # app.register_blueprint(customer_bp, url_prefix='/mechanics')
    # app.register_blueprint(customer_bp, url_prefix='/ServiceTickets')

    return app