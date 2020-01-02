from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField, SelectField, TextAreaField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from TrendieSrc.models import User

class RegistrationForm(FlaskForm):
    username = TextField('Username', validators=[DataRequired(), Length(min=5, max=20)])
    email = TextField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password',  validators=[DataRequired()] )
    password_confirm = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        if User.query.filter_by(username=username.data).first():
            raise ValidationError('Username already registered. Please use a different username')

    def validate_email(self, email):
        if User.query.filter_by(email=email.data).first():
            raise ValidationError('Email already registered. Please use a different email')


class LoginForm(FlaskForm):
    email = TextField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class PostForm(FlaskForm):
    title = TextField('Title', validators=[DataRequired(), Length(min=3, max=30) ])
    category =  SelectField('Category', choices=[('Entertainment','Entertainment'), ('Food', 'Food'), ('Gaming', 'Gaming'), ('Health', 'Health'), ('Lifestyle', 'Lifestyle'), ('Shopping', 'Shopping'), ('Sport','Sport'), ('Technology','Technology'), ('Travel','Travel'), ('Other','Other')] )
    reference = TextField('Reference')
    content = TextAreaField('Content', validators=[DataRequired()])
    private = BooleanField('Private', default=False)
    submit = SubmitField('Post')

