from flask import Flask, session, render_template
from datetime import datetime
from flask_wtf.csrf import CSRFProtect
from config import config
from models import db

csrf = CSRFProtect()
from models.user import User
from models.post import Post
from models.comment import Comment
from models.like import PostLike
from models.preference import UserPreference
from routes import auth_bp, main_bp, posts_bp, api_bp
import os

def nl2br(value):
    if value is None:
        return ''
    return str(value).replace('\n', '<br>\n')

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    os.makedirs(app.instance_path, exist_ok=True)

    db.init_app(app)
    csrf.init_app(app)

    app.jinja_env.filters['nl2br'] = nl2br

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(posts_bp)
    app.register_blueprint(api_bp)

    @app.before_request
    def load_theme():
        if 'user_id' in session and 'theme' not in session:
            from models.preference import UserPreference
            preference = UserPreference.query.filter_by(user_id=session['user_id']).first()
            if preference:
                session['theme'] = preference.theme
            else:
                session['theme'] = 'light'

    @app.errorhandler(404)
    def not_found(error):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return render_template('errors/500.html'), 500

    with app.app_context():
        db.create_all()

    return app

if __name__ == '__main__':
    app = create_app(os.environ.get('FLASK_ENV', 'development'))
    app.run(host='0.0.0.0', port=5000, debug=True)
