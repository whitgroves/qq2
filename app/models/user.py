from app.extensions import db
from sqlalchemy.sql import func, expression

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(80), nullable=False, unique=True)
    # age = db.Column(db.Integer)
    # bio = db.Column(db.Text)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now()) # func.now() renders as CURRENT_TIMESTAMP at table creation
    active = db.Column(db.Boolean, nullable=False, server_default=expression.true())
    # posts = db.relationship('Post', backref='user')
    # comments = db.relationship('Comment', backref='user')

    def __repr__(self):
        return f'<User {self.username}{' (inactive)' if not self.active else ''}>'
