from flask import Flask
from config import Config
from extensions import db, login_manager, socketio

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'pages.login'
    socketio.init_app(app)

    # Register Blueprints
    from routes.auth import auth_bp
    from routes.api import api_bp
    from routes.pages import pages_bp
    
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(pages_bp)

    return app

if __name__ == '__main__':
    app = create_app()
    socketio.run(app, debug=True)
