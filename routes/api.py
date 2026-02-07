from flask import Blueprint, request, jsonify, session
from models import db
from models.post import Post
from models.comment import Comment
from models.like import PostLike
from utils import login_required
from datetime import datetime

api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route('/posts/<int:post_id>/like', methods=['POST'])
@login_required
def like_post(post_id):
    post = Post.query.get_or_404(post_id)

    existing_like = PostLike.query.filter_by(
        post_id=post_id,
        user_id=session['user_id']
    ).first()

    if existing_like:
        if existing_like.like_type == 'like':
            db.session.delete(existing_like)
            action = 'removed'
        else:
            existing_like.like_type = 'like'
            action = 'changed'
    else:
        new_like = PostLike(post_id=post_id, user_id=session['user_id'], like_type='like')
        db.session.add(new_like)
        action = 'added'

    db.session.commit()

    return jsonify({
        'success': True,
        'action': action,
        'like_count': post.get_like_count(),
        'dislike_count': post.get_dislike_count()
    })

@api_bp.route('/posts/<int:post_id>/dislike', methods=['POST'])
@login_required
def dislike_post(post_id):
    post = Post.query.get_or_404(post_id)

    existing_like = PostLike.query.filter_by(
        post_id=post_id,
        user_id=session['user_id']
    ).first()

    if existing_like:
        if existing_like.like_type == 'dislike':
            db.session.delete(existing_like)
            action = 'removed'
        else:
            existing_like.like_type = 'dislike'
            action = 'changed'
    else:
        new_like = PostLike(post_id=post_id, user_id=session['user_id'], like_type='dislike')
        db.session.add(new_like)
        action = 'added'

    db.session.commit()

    return jsonify({
        'success': True,
        'action': action,
        'like_count': post.get_like_count(),
        'dislike_count': post.get_dislike_count()
    })

@api_bp.route('/posts/<int:post_id>/comments', methods=['GET', 'POST'])
@login_required
def comments(post_id):
    post = Post.query.get_or_404(post_id)

    if request.method == 'POST':
        content = request.form.get('content', '').strip()

        if not content:
            return jsonify({'success': False, 'error': 'Comment cannot be empty'}), 400

        comment = Comment(
            post_id=post_id,
            user_id=session['user_id'],
            content=content
        )

        db.session.add(comment)
        db.session.commit()

        return jsonify({
            'success': True,
            'comment': {
                'id': comment.id,
                'content': comment.content,
                'author': session['username'],
                'created_at': comment.created_at.strftime('%Y-%m-%d %H:%M')
            }
        })

    comments = Comment.query.filter_by(post_id=post_id)\
        .order_by(Comment.created_at.asc()).all()

    return jsonify({
        'success': True,
        'comments': [{
            'id': c.id,
            'content': c.content,
            'author': c.author.username,
            'created_at': c.created_at.strftime('%Y-%m-%d %H:%M'),
            'can_delete': c.user_id == session.get('user_id')
        } for c in comments]
    })

@api_bp.route('/comments/<int:comment_id>', methods=['DELETE'])
@login_required
def delete_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)

    if comment.user_id != session['user_id']:
        return jsonify({'success': False, 'error': 'Unauthorized'}), 403

    db.session.delete(comment)
    db.session.commit()

    return jsonify({'success': True})

@api_bp.route('/search', methods=['POST'])
def search():
    query = request.form.get('query', '').strip()

    if not query:
        return jsonify({'success': False, 'error': 'Query required'}), 400

    posts = Post.query.filter(
        Post.published == True,
        db.or_(
            Post.title.contains(query),
            Post.content.contains(query),
            Post.summary.contains(query)
        )
    ).order_by(Post.created_at.desc()).limit(20).all()

    return jsonify({
        'success': True,
        'results': [{
            'id': p.id,
            'title': p.title,
            'summary': p.summary,
            'author': p.author.username,
            'created_at': p.created_at.strftime('%Y-%m-%d')
        } for p in posts]
    })
