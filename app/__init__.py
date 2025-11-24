from flask import Flask
from flask_login import LoginManager

login_manager = LoginManager()


def create_app(config_name='default'):
    """Create and configure the Flask application."""
    
    app = Flask(__name__, template_folder='templates')
    
    # Secret key for session security
    app.config['SECRET_KEY'] = 'dev-secret-key-change-in-production'
    
    # This is important - set session cookie settings
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
    
    if config_name == 'testing':
        app.config['TESTING'] = True
    
    # Initialize Flask-Login
    login_manager.init_app(app)
    login_manager.login_view = 'main.login'
    
    
    from app.models import get_user_by_id
    
    @login_manager.user_loader
    def load_user(user_id):
        user = get_user_by_id(user_id)
        return user
    
    # Register routes
    from app.routes import main
    app.register_blueprint(main)
    
    return app