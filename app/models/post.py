from app.extensions import db
from sqlalchemy.sql import func

# many-to-many
post_tag = db.Table('post_tag',
                    db.Column('post_id', db.Integer, db.ForeignKey('post.id')),
                    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')))

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    content = db.Column(db.Text)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    # comments = db.relationship('Comment', backref='post')
    tags = db.relationship('Tag', secondary=post_tag, backref='posts')

    def __repr__(self):
        return f'<Post {self.id}: "{self.title}">'
#endclass