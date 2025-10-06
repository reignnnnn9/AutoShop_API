from flask import Flask
from .models import db
from .extensions import ma, limiter, cache
from .blueprints.customers import customer_bp
from .blueprints.mechanics import mechanic_bp
from .blueprints.service_tickets import ticket_bp
from .blueprints.parts import part_bp
from flask_swagger_ui import get_swaggerui_blueprint

SWAGGER_URL = '/api/docs'  # URL for exposing Swagger UI (without trailing '/')
API_URL = '/static/swagger.yaml'  # Our API URL (can of course be a local resource)

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Mechanic API"
    }
)

def create_app(config_name):

    app = Flask(__name__)
    app.config.from_object(f'config.{config_name}')

    # Initialize extensions - plugging them in 
    db.init_app(app)
    ma.init_app(app)
    limiter.init_app(app)
    cache.init_app(app)

    # Register Blueprints
    app.register_blueprint(customer_bp, url_prefix='/customers')
    app.register_blueprint(mechanic_bp, url_prefix='/mechanics')
    app.register_blueprint(ticket_bp, url_prefix='/service_tickets')
    app.register_blueprint(part_bp, url_prefix='/parts')
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

    return app