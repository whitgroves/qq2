from app.extensions import db
from sqlalchemy.sql import func

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))

    def __repr__(self):
        return f'<Comment {self.id}: "{self.content[:20]}{'...' if len(self.content) > 20 else ''}">'
#endclass