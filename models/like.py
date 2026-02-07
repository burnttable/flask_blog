from . import db

class PostLike(db.Model):
    __tablename__ = 'post_likes'

    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    like_type = db.Column(db.String(10), nullable=False)  # 'like' or 'dislike'

    __table_args__ = (db.UniqueConstraint('post_id', 'user_id', name='unique_post_user_like'),)

    def __repr__(self):
        return f'<PostLike post={self.post_id} user={self.user_id} type={self.like_type}>'
