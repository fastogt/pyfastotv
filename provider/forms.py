from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import InputRequired, Length, Email

import pyfastocloud_models.constants as constants


class SignUpForm(FlaskForm):
    email = StringField('Email:',
                        validators=[InputRequired(), Email(message='Invalid email'), Length(max=30)])
    first_name = StringField('First name:', validators=[InputRequired(), Length(max=64)])
    last_name = StringField('Last name:', validators=[InputRequired(), Length(max=64)])
    password = PasswordField('Password:', validators=[InputRequired(), Length(min=3, max=80)])
    country = SelectField('Country:', coerce=str, validators=[InputRequired()],
                          choices=constants.AVAILABLE_COUNTRIES)
    language = SelectField('Language:', coerce=str, default=constants.DEFAULT_LOCALE,
                           choices=constants.AVAILABLE_LOCALES_PAIRS)
    submit = SubmitField('Sign Up')


class SignInForm(FlaskForm):
    email = StringField('Email:',
                        validators=[InputRequired(), Email(message='Invalid email'), Length(max=30)])
    password = PasswordField('Password:', validators=[InputRequired(), Length(min=3, max=80)])
    submit = SubmitField('Sign In')
