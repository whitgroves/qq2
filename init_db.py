from app import create_app
from app.extensions import db
from app.models.users import User
from app.models.posts import Post, Tag, Comment
from werkzeug.security import generate_password_hash

with create_app().app_context():
    db.drop_all()
    db.create_all()
    
    users = [User(username=f'user{i}', 
                  email=f'user{i}@example.com', 
                  password=generate_password_hash(f'password{i}')) for i in range(1, 11)]
    
    posts = [Post(title=f'Post #{i}', 
                  content=f'This is post # {i}', 
                  user_id=(i//10 + 1)) for i in range(1, 100)]

    comments = [
        Comment(content='Comment for the first post', post=posts[0], user=users[0]),
        Comment(content='Comment for the second post', post=posts[1], user_id=1),
        Comment(content='Another comment for the second post', post_id=2, user=users[2]),
        Comment(content='Another comment for the first post', post_id=1, user_id=3),
    ]

    tags = [Tag(name=n) for n in ['animals', 'tech', 'cooking', 'writing']]
    posts[0].tags.extend([tags[0], tags[3]])
    posts[2].tags.extend([tags[2], tags[1], tags[3]])

    db.session.add_all(users)
    db.session.add_all(posts)
    db.session.add_all(comments)
    db.session.add_all(tags)
    db.session.commit()
