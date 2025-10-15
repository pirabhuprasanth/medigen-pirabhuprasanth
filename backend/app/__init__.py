# backend/app/__init__.py
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from .models import db
from config import config_map
from .routes import api_bp
import os

def create_app(config_name=None):
    # Application factory function
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')
    
    app = Flask(__name__)
    app.config.from_object(config_map.get(config_name, config_map['default']))

    # Initialize extensions
    CORS(app, 
         origins=app.config.get('CORS_ORIGINS', ['http://localhost:3000']),
         supports_credentials=True)  # Enable Cross-Origin Resource Sharing
    
    jwt = JWTManager(app)
    db.init_app(app)
    
    # JWT error handlers
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return {'error': 'Token has expired', 'message': 'Please login again'}, 401
    
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return {'error': 'Invalid token', 'message': 'Please provide a valid token'}, 401
    
    @jwt.unauthorized_loader
    def unauthorized_callback(error):
        return {'error': 'Authorization required', 'message': 'Please login to access this resource'}, 401

    # Register blueprints
    app.register_blueprint(api_bp, url_prefix='/api')
    
    # Health check route
    @app.route('/')
    def health_check():
        return {
            'message': 'MediCare API is running',
            'version': app.config.get('API_VERSION', '1.0.0'),
            'status': 'healthy'
        }

    return app