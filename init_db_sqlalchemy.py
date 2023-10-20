from app import app, db, Post, Comment, Tag

with app.app_context(): # SQLAlchemy requires an active app context for db operations
    db.drop_all()
    db.create_all()

    posts = [Post(title=f'Post #{i}', content=f'This is post numero {i}') for i in range(1, 4)]
    comments = [
        Comment(content='Comment for the first post', post=posts[0]),
        Comment(content='Comment for the second post', post=posts[1]),
        Comment(content='Another comment for the second post', post_id=2),
        Comment(content='Another comment for the first post', post_id=1),
    ]
    tags = [Tag(name=n) for n in ['animals', 'tech', 'cooking', 'writing']]
    posts[0].tags.extend([tags[0], tags[3]])
    posts[2].tags.extend([tags[2], tags[1], tags[3]])

    db.session.add_all(posts)
    db.session.add_all(comments)
    db.session.add_all(tags)
    db.session.commit()