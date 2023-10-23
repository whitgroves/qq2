from app import create_app
from app.extensions import db
from app.models.users import User
from app.models.posts import Post, Tag, Comment
from werkzeug.security import generate_password_hash
from random import choice, choices, randint

with create_app().app_context():
    db.drop_all()
    db.create_all()
    
    users = [User(username=f'user{i}', email=f'user{i}@example.com', 
                  password=generate_password_hash(f'password{i}')) for i in range(1, 5)]
    
    posts = [Post(title=f'Post number {i}', content=f'This is post number {i}', 
                  user_id=(i//10 + 1)) for i in range(1, 40)]
    
    comments = [Comment(content='first', post=p, user=choice(users)) for p in posts]

    tags = [Tag(name=n) for n in ['animals', 'tech', 'cooking', 'writing']]
    [p.tags.extend(choices(tags, k=randint(1, len(tags)))) for p in posts]

    db.session.add_all(users)
    db.session.add_all(posts)
    db.session.add_all(comments)
    db.session.add_all(tags)
    db.session.commit()
