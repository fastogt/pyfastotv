import pyfastocloud_models.constants as constants
from flask_wtf import FlaskForm
from pyfastocloud_models.service.entry import ServiceSettings, ProviderPair
from wtforms.fields import StringField, SubmitField, MultipleFileField, SelectField, FormField, FloatField
from wtforms.validators import InputRequired, Length, Email

from app.common.common_forms import HostAndPortForm


class ServiceSettingsForm(FlaskForm):
    name = StringField('Name:', validators=[InputRequired()])
    host = FormField(HostAndPortForm, 'Host:', validators=[])
    http_host = FormField(HostAndPortForm, 'Http host:', validators=[])
    vods_host = FormField(HostAndPortForm, 'Vods host:', validators=[])
    cods_host = FormField(HostAndPortForm, 'Cods host:', validators=[])

    feedback_directory = StringField('Feedback directory:', validators=[InputRequired()])
    timeshifts_directory = StringField('Timeshifts directory:', validators=[InputRequired()])
    hls_directory = StringField('Hls directory:', validators=[InputRequired()])
    vods_directory = StringField('Vods out directory:', validators=[InputRequired()])
    cods_directory = StringField('Cods out directory:', validators=[InputRequired()])
    proxy_directory = StringField('Proxy out directory:', validators=[InputRequired()])
    apply = SubmitField('Apply')

    def make_entry(self):
        return self.update_entry(ServiceSettings())

    def update_entry(self, settings: ServiceSettings):
        settings.name = self.name.data
        settings.host = self.host.get_data()
        settings.http_host = self.http_host.get_data()
        settings.vods_host = self.vods_host.get_data()
        settings.cods_host = self.cods_host.get_data()

        settings.feedback_directory = self.feedback_directory.data
        settings.timeshifts_directory = self.timeshifts_directory.data
        settings.hls_directory = self.hls_directory.data
        settings.vods_directory = self.vods_directory.data
        settings.cods_directory = self.cods_directory.data
        settings.proxy_directory = self.proxy_directory.data
        settings.monitoring = False
        return settings


class ActivateForm(FlaskForm):
    LICENSE_KEY_LENGTH = 97

    license = StringField('License:',
                          validators=[InputRequired(), Length(min=LICENSE_KEY_LENGTH, max=LICENSE_KEY_LENGTH)])
    submit = SubmitField('Activate')


class UploadM3uForm(FlaskForm):
    AVAILABLE_STREAM_TYPES_FOR_UPLOAD = [(constants.StreamType.PROXY, 'Proxy Stream'),
                                         (constants.StreamType.VOD_PROXY, 'Proxy Vod'),
                                         (constants.StreamType.RELAY, 'Relay'),
                                         (constants.StreamType.ENCODE, 'Encode'),
                                         (constants.StreamType.CATCHUP, 'Catchup'),
                                         (constants.StreamType.TEST_LIFE, 'Test life'),
                                         (constants.StreamType.VOD_RELAY, 'Vod relay'),
                                         (constants.StreamType.VOD_ENCODE, 'Vod encode'),
                                         (constants.StreamType.COD_RELAY, 'Cod relay'),
                                         (constants.StreamType.COD_ENCODE, 'Cod encode'),
                                         (constants.StreamType.EVENT, 'Event')]

    files = MultipleFileField()
    type = SelectField('Type:', coerce=constants.StreamType.coerce, validators=[InputRequired()],
                       choices=AVAILABLE_STREAM_TYPES_FOR_UPLOAD, default=constants.StreamType.RELAY)
    upload = SubmitField('Upload')


class ServerProviderForm(FlaskForm):
    AVAILABLE_ROLES = [(ProviderPair.Roles.READ, 'Read'), (ProviderPair.Roles.WRITE, 'Write'),
                       (ProviderPair.Roles.SUPPORT, 'Support'), (ProviderPair.Roles.ADMIN, 'Admin')]

    email = StringField('Email:',
                        validators=[InputRequired(), Email(message='Invalid email'), Length(max=30)])
    role = SelectField('Role:', coerce=ProviderPair.Roles.coerce, validators=[InputRequired()],
                       choices=AVAILABLE_ROLES, default=ProviderPair.Roles.ADMIN)
    apply = SubmitField('Apply')
