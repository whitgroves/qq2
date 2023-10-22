from app.models.shared import *

post_tag = db.Table('post_tag',
                    Column('post_id', Integer, ForeignKey('post.id')),
                    Column('tag_id', Integer, ForeignKey('tag.id')))

class Post(db.Model):
    id = Column(Integer, primary_key=True)
    title = Column(String(100))
    content = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    comments = db.relationship('Comment', backref='post')
    tags = db.relationship('Tag', secondary=post_tag, backref='posts')

    def __repr__(self):
        return f'<Post {self.id}: "{self.title}">'

class Tag(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)

    def __repr__(self):
        return f'<Tag "{self.name}">'

class Comment(db.Model):
    id = Column(Integer, primary_key=True)
    content = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    post_id = Column(Integer, ForeignKey('post.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'<Comment {self.id}: "{self.content[:20]}{'...' if len(self.content) > 20 else ''}">'
