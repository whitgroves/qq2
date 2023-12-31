"""Secured web forms for qq2.

Note that the first parameter of each Field object is the displayed label text.
For more info see:
    - https://wtforms.readthedocs.io/en/3.1.x/ (WTForms)
    - https://flask-wtf.readthedocs.io/en/0.15.x/ (Flask-WTF)

For standard usage, see app/templates/login.html
"""
import wtforms
import wtforms.validators
import flask_wtf

def input_required(max_len:int=None) -> list:
    """Helps build validator lists for required fields."""
    validators = [wtforms.validators.InputRequired()]
    if max_len is not None:
        validators.append(wtforms.validators.Length(max=max_len))

# users/id/edit
class UserForm(flask_wtf.FlaskForm):
    email = wtforms.EmailField('Email', validators=input_required(80))
    username = wtforms.StringField('Username', validators=input_required(100))
    bio = wtforms.TextAreaField('Bio')

# posts/new (post)
class PostForm(flask_wtf.FlaskForm):
    title = wtforms.StringField('Title', validators=input_required(100))
    content = wtforms.TextAreaField('Content', validators=input_required())
    tags = wtforms.StringField('Tags (separated by comma)')

# posts/id (comment)
class CommentForm(flask_wtf.FlaskForm):
    content = wtforms.TextAreaField('Comment', validators=input_required())

# register
class RegisterForm(flask_wtf.FlaskForm):
    email = wtforms.EmailField('Email', validators=input_required(80))
    password = wtforms.PasswordField('Password', validators=input_required(100))
    username = wtforms.StringField('Username', validators=input_required(100))

# login
class LoginForm(flask_wtf.FlaskForm):
    user_email = wtforms.StringField('Username or Email',
                                     validators=input_required())
    password = wtforms.PasswordField('Password', validators=input_required())
    remember = wtforms.BooleanField('Remember me?')
