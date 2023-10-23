from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField
from wtforms.validators import InputRequired, Length

# NOTE: first param of each field is the displayed label text

# users/id/edit
class UserForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Length(max=80)])
    username = StringField('Username', validators=[InputRequired(), Length(max=100)])
    bio = TextAreaField('Bio')

# posts/id (comment)
class CommentForm(FlaskForm):
    content = TextAreaField('Comment', validators=[InputRequired()])

# register
class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Length(max=80)])
    password = StringField('Password', validators=[InputRequired(), Length(max=100)])
    username = StringField('Username', validators=[InputRequired(), Length(max=100)])

# login
class LoginForm(FlaskForm):
    user_email = StringField('Username or Email', validators=[InputRequired()])
    password = StringField('Password', validators=[InputRequired()])
    remember = BooleanField('Remember me?')