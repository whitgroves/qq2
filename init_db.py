from app import create_app
from app.extensions import db
from app.models.user import User
from app.models.post import Post
from app.models.tag import Tag

with create_app().app_context():
    db.drop_all()
    db.create_all()
    
    users = [User(username=f'user{i}', email=f'user{i}@example.com') for i in range(1, 11)]
    posts = [Post(title=f'Post #{i}', content=f'This is post numero {i}') for i in range(1, 101)]
    tags = [Tag(name=n) for n in ['animals', 'tech', 'cooking', 'writing']]

    posts[0].tags.extend([tags[0], tags[3]])
    posts[2].tags.extend([tags[2], tags[1], tags[3]])

    db.session.add_all(users)
    db.session.add_all(posts)
    db.session.add_all(tags)
    db.session.commit()
