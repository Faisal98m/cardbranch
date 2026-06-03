import os
from pathlib import Path
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import config_map

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'


def create_app(config_name=None):
    if config_name is None:
        config_name = os.environ.get('FLASK_CONFIG', 'Debug')

    _root = Path(__file__).resolve().parent.parent
    app = Flask(__name__,
                template_folder=str(_root / 'templates'),
                static_folder=str(_root / 'static'),
                static_url_path='/static')
    app.config.from_object(config_map[config_name])

    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['GENERATED_FOLDER'], exist_ok=True)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    from app.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from app.auth.routes import auth_bp
    from app.public.routes import public_bp
    from app.dashboard.routes import dashboard_bp
    from app.admin.routes import admin_bp
    from app.checkout.routes import checkout_bp

    app.register_blueprint(auth_bp, url_prefix='/')
    app.register_blueprint(public_bp, url_prefix='/')
    app.register_blueprint(dashboard_bp, url_prefix='/')
    app.register_blueprint(admin_bp, url_prefix='/')
    app.register_blueprint(checkout_bp, url_prefix='/')

    @app.context_processor
    def inject_r2_url():
        import os
        return {'r2_url': os.environ.get('R2_PUBLIC_URL', '').rstrip('/')}

    with app.app_context():
        db.create_all()

    return app
