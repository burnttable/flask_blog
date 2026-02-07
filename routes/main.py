from flask import Blueprint, render_template, session, redirect, url_for, request
from models import db
from models.post import Post
from models.preference import UserPreference
from models.user import User
from utils import login_required

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    per_page = 10

    posts = Post.query.filter_by(published=True)\
        .order_by(Post.created_at.desc())\
        .paginate(page=page, per_page=per_page, error_out=False)

    return render_template('index.html', posts=posts)

@main_bp.route('/theme/toggle')
@login_required
def toggle_theme():
    current_theme = session.get('theme', 'light')
    new_theme = 'dark' if current_theme == 'light' else 'light'

    session['theme'] = new_theme

    preference = UserPreference.query.filter_by(user_id=session['user_id']).first()
    if preference:
        preference.theme = new_theme
        db.session.commit()

    next_page = request.referrer or url_for('main.index')
    return redirect(next_page)
