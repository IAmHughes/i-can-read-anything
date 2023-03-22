from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, Optional

# List of languages (replace this with the actual list of languages you want to support)
languages = ['English', 'Spanish', 'French', 'German', 'Chinese']

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')
    
def custom_coerce(value):
    if value == '':
        return None
    return int(value)

class ProfileForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('New Password', validators=[Optional()])
    confirm_password = PasswordField('Confirm New Password', validators=[EqualTo('password')])
    bio = TextAreaField('Bio', validators=[Length(max=500)])
    language = SelectField('Language', choices=[('', 'Select a language')] + [(str(i), lang) for i, lang in enumerate(languages)], validators=[Optional()])
    proficiency = SelectField('Proficiency', choices=[('', 'Select proficiency')] + [(str(i), str(i)) for i in range(1, 6)], coerce=custom_coerce, validators=[Optional()])
    submit = SubmitField('Update Profile')