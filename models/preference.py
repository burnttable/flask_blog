from . import db

class UserPreference(db.Model):
    __tablename__ = 'user_preferences'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    theme = db.Column(db.String(10), default='light', nullable=False)

    def __repr__(self):
        return f'<UserPreference user={self.user_id} theme={self.theme}>'
