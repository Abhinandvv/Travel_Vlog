from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from travel.models import User
class RegistrationForm(FlaskForm):
    username = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('UserName Already Exists')
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email Already Exists')
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remeber me')
    submit = SubmitField('Login')
class UpdateAccountForm(FlaskForm):
    username = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')
    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('UserName Already Exists')
    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Email Already Exists')
class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    place = StringField('Place', validators=[DataRequired()])
    picture = FileField('Upload Picture', validators=[DataRequired(), FileAllowed(['jpg', 'png'])])
    picture2 = FileField('Upload Picture', validators=[FileAllowed(['jpg', 'png'])])
    picture3 = FileField('Upload Picture', validators=[FileAllowed(['jpg', 'png'])])
    picture4 = FileField('Upload Picture', validators=[FileAllowed(['jpg', 'png'])])
    content =  TextAreaField('Content', validators=[DataRequired()])
    content2 =  TextAreaField('Content')
    content3 =  TextAreaField('Content')
    content4 =  TextAreaField('Content')
    submit = SubmitField('Post Now')
class UpdateForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    place = StringField('Place')
    picture = FileField('Upload Picture', validators=[FileAllowed(['jpg', 'png'])])
    picture2 = FileField('Upload Picture', validators=[FileAllowed(['jpg', 'png'])])
    picture3 = FileField('Upload Picture', validators=[FileAllowed(['jpg', 'png'])])
    picture4 = FileField('Upload Picture', validators=[FileAllowed(['jpg', 'png'])])
    content =  TextAreaField('Content', validators=[DataRequired()])
    content2 =  TextAreaField('Content')
    content3 =  TextAreaField('Content')
    content4 =  TextAreaField('Content')
    submit = SubmitField('Update Post')

class FeedbackForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    subject = StringField('Name', validators=[DataRequired()])
    message =  TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Send Message')