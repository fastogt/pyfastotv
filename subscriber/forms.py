import pyfastocloud_models.constants as constants
from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, SubmitField, SelectField, IntegerField, DateTimeField
from wtforms.validators import InputRequired, Length, Email, NumberRange
from app.home.entry import SubscriberUser


class SignUpForm(FlaskForm):
    AVAILABLE_STATUSES = [(SubscriberUser.Status.NOT_ACTIVE, 'Not active'), (SubscriberUser.Status.ACTIVE, 'Active'),
                          (SubscriberUser.Status.DELETED, 'Deleted')]

    email = StringField('Email:',
                        validators=[InputRequired(), Email(message='Invalid email'), Length(max=30)])
    first_name = StringField('First name:', validators=[InputRequired(), Length(max=30)])
    last_name = StringField('Last name:', validators=[InputRequired(), Length(max=30)])
    password = PasswordField('Password:', validators=[InputRequired(), Length(min=3, max=80)])
    country = SelectField('Country:', coerce=str, validators=[InputRequired()],
                          choices=constants.AVAILABLE_COUNTRIES)
    language = SelectField('Language:', coerce=str, default=constants.DEFAULT_LOCALE,
                           choices=constants.AVAILABLE_LOCALES_PAIRS)
    status = SelectField('Status:', coerce=SubscriberUser.Status.coerce, validators=[InputRequired()],
                         choices=AVAILABLE_STATUSES)
    exp_date = DateTimeField(default=SubscriberUser.MAX_DATE)
    max_devices_count = IntegerField('Max devices count:', default=constants.DEFAULT_DEVICES_COUNT,
                                     validators=[NumberRange(1, 100)])
    apply = SubmitField('Sign Up')

    def validate_password(self, validate: bool):
        if validate:
            self.password.validators = [InputRequired(), Length(min=3, max=80)]
        else:
            self.password.validators = []

    def make_entry(self) -> SubscriberUser:
        return self.update_entry(SubscriberUser())

    def update_entry(self, subscriber: SubscriberUser) -> SubscriberUser:
        subscriber.email = self.email.data.lower()
        subscriber.first_name = self.first_name.data
        subscriber.last_name = self.last_name.data
        subscriber.password = SubscriberUser.generate_password_hash(self.password.data)
        subscriber.country = self.country.data
        subscriber.language = self.language.data
        subscriber.status = self.status.data
        subscriber.exp_date = self.exp_date.data
        subscriber.max_devices_count = self.max_devices_count.data
        return subscriber


class SignInForm(FlaskForm):
    email = StringField('Email:',
                        validators=[InputRequired(), Email(message='Invalid email'), Length(max=30)])
    password = PasswordField('Password:', validators=[InputRequired(), Length(min=3, max=80)])
    submit = SubmitField('Sign In')
