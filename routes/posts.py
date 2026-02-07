from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify
from models import db
from models.post import Post
from models.comment import Comment
from models.user import User
from utils import login_required
from utils.helpers import truncate_text
from datetime import datetime

posts_bp = Blueprint('posts', __name__, url_prefix='/posts')

@posts_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '').strip()
        publish = request.form.get('publish', 'off') == 'on'

        if not title or not content:
            flash('Title and content are required.', 'danger')
            return render_template('posts/create.html')

        summary = truncate_text(content, 200)

        post = Post(
            title=title,
            content=content,
            summary=summary,
            user_id=session['user_id'],
            published=publish
        )

        db.session.add(post)
        db.session.commit()

        action = 'published' if publish else 'saved as draft'
        flash(f'Post {action} successfully!', 'success')
        return redirect(url_for('posts.view', id=post.id))

    return render_template('posts/create.html')

@posts_bp.route('/<int:post_id>')
def view(post_id):
    post = Post.query.get_or_404(post_id)

    if not post.published and post.user_id != session.get('user_id'):
        flash('This post is not published.', 'warning')
        return redirect(url_for('main.index'))

    post.view_count += 1
    db.session.commit()

    comments = Comment.query.filter_by(post_id=post_id)\
        .order_by(Comment.created_at.asc()).all()

    user_like = None
    if 'user_id' in session:
        from models.like import PostLike
        user_like = PostLike.query.filter_by(
            post_id=post_id,
            user_id=session['user_id']
        ).first()

    return render_template('posts/view.html', post=post, comments=comments, user_like=user_like)

@posts_bp.route('/<int:post_id>/edit', methods=['GET', 'POST'])
@login_required
def edit(post_id):
    post = Post.query.get_or_404(post_id)

    if post.user_id != session['user_id']:
        flash('You can only edit your own posts.', 'danger')
        return redirect(url_for('posts.view', id=post_id))

    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '').strip()
        publish = request.form.get('publish', 'off') == 'on'

        if not title or not content:
            flash('Title and content are required.', 'danger')
            return render_template('posts/edit.html', post=post)

        post.title = title
        post.content = content
        post.summary = truncate_text(content, 200)
        post.published = publish
        post.updated_at = datetime.utcnow()

        db.session.commit()

        action = 'published' if publish else 'saved as draft'
        flash(f'Post {action} successfully!', 'success')
        return redirect(url_for('posts.view', id=post_id))

    return render_template('posts/edit.html', post=post)

@posts_bp.route('/<int:post_id>/publish', methods=['POST'])
@login_required
def publish(post_id):
    post = Post.query.get_or_404(post_id)

    if post.user_id != session['user_id']:
        flash('You can only publish your own posts.', 'danger')
        return redirect(url_for('posts.view', id=post_id))

    post.published = True
    db.session.commit()

    flash('Post published successfully!', 'success')
    return redirect(url_for('posts.view', id=post_id))

@posts_bp.route('/<int:post_id>/delete', methods=['POST'])
@login_required
def delete(post_id):
    post = Post.query.get_or_404(post_id)

    if post.user_id != session['user_id']:
        flash('You can only delete your own posts.', 'danger')
        return redirect(url_for('posts.view', id=post_id))

    db.session.delete(post)
    db.session.commit()

    flash('Post deleted successfully!', 'success')
    return redirect(url_for('main.index'))

@posts_bp.route('/my')
@login_required
def my_posts():
    page = request.args.get('page', 1, type=int)
    per_page = 10

    posts = Post.query.filter_by(user_id=session['user_id'])\
        .order_by(Post.created_at.desc())\
        .paginate(page=page, per_page=per_page, error_out=False)

    return render_template('index.html', posts=posts, my_posts=True)
