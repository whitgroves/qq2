from app.models.shared import *
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = Column(Integer, primary_key=True)
    email = Column(String(80), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    username = Column(String(100), nullable=False)
    bio = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now()) # CURRENT_TIMESTAMP
    # active = Column(Boolean, nullable=False, server_default=expression.true())
    posts = db.relationship('Post', backref='user', cascade='all, delete-orphan')
    comments = db.relationship('Comment', backref='user', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<User {self.username}{' (inactive)' if not self.active else ''}>'
