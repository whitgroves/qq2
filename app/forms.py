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
    """Update form for user information."""
    email = wtforms.EmailField('Email', validators=input_required(80))
    username = wtforms.StringField('Username', validators=input_required(100))
    bio = wtforms.TextAreaField('Bio')

# posts/id (comment)
class CommentForm(flask_wtf.FlaskForm):
    """Comment form."""
    content = wtforms.TextAreaField('Comment', validators=input_required())

# register
class RegisterForm(flask_wtf.FlaskForm):
    """Registration form for new users."""
    email = wtforms.EmailField('Email', validators=input_required(80))
    password = wtforms.PasswordField('Password', validators=input_required(100))
    username = wtforms.StringField('Username', validators=input_required(100))

# login
class LoginForm(flask_wtf.FlaskForm):
    """Login form for returning users."""
    user_email = wtforms.StringField('Username or Email', validators=input_required())
    password = wtforms.PasswordField('Password', validators=input_required())
    remember = wtforms.BooleanField('Remember me?')
