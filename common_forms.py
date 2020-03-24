import pyfastocloud_models.constants as constants
from pyfastocloud_models.common_entries import Rational, Size, Logo, RSVGLogo, HostAndPort, HttpProxy
from wtforms import Form
from wtforms.fields import StringField, IntegerField, FormField, FloatField, SelectField, BooleanField, Field
from wtforms.validators import InputRequired, Length, NumberRange
from wtforms.widgets import TextInput


class UrlForm(Form):
    id = IntegerField('Id:', validators=[InputRequired()], render_kw={'readonly': 'true'})
    uri = StringField('Url:', validators=[InputRequired(),
                                          Length(min=constants.MIN_URL_LENGTH, max=constants.MAX_URL_LENGTH)])


class HttpProxyForm(Form):
    url = StringField('Url:', validators=[])
    user = StringField('User:', validators=[])
    password = StringField('Password:', validators=[])

    def get_data(self) -> HttpProxy:
        proxy = HttpProxy()
        proxy_data = self.data
        proxy.path = proxy_data['url']
        proxy.x = proxy_data['user']
        proxy.y = proxy_data['password']
        return proxy


class InputUrlForm(UrlForm):
    AVAILABLE_USER_AGENTS = [(constants.UserAgent.GSTREAMER, 'GStreamer'), (constants.UserAgent.VLC, 'VLC'),
                             (constants.UserAgent.FFMPEG, 'FFmpeg'), (constants.UserAgent.WINK, 'Wink'),
                             (constants.UserAgent.CHROME, 'Chrome'), (constants.UserAgent.MOZILLA, 'Mozilla'),
                             (constants.UserAgent.SAFARI, 'Safari')]

    user_agent = SelectField('User agent:', validators=[InputRequired()], choices=AVAILABLE_USER_AGENTS,
                             coerce=constants.UserAgent.coerce)
    stream_link = BooleanField('SteamLink:', validators=[])
    proxy = FormField(HttpProxyForm, 'Http proxy:', validators=[])


class OutputUrlForm(UrlForm):
    AVAILABLE_HLS_TYPES = [(constants.HlsType.HLS_PULL, 'PULL'), (constants.HlsType.HLS_PUSH, 'PUSH')]

    http_root = StringField('Http root:',
                            validators=[InputRequired(),
                                        Length(min=constants.MIN_PATH_LENGTH, max=constants.MAX_PATH_LENGTH)],
                            render_kw={'readonly': 'true'})
    hls_type = SelectField('HLS Type:', validators=[InputRequired()], choices=AVAILABLE_HLS_TYPES,
                           coerce=constants.HlsType.coerce)


class SizeForm(Form):
    width = IntegerField('Width:', validators=[InputRequired()])
    height = IntegerField('Height:', validators=[InputRequired()])

    def get_data(self) -> Size:
        size = Size()
        size_data = self.data
        size.width = size_data['width']
        size.height = size_data['height']
        return size


class RSVGLogoForm(Form):
    path = StringField('Path:', validators=[])
    x = IntegerField('Pos x:', validators=[InputRequired()])
    y = IntegerField('Pos y:', validators=[InputRequired()])
    size = FormField(SizeForm, 'Size:', validators=[])

    def get_data(self) -> RSVGLogo:
        logo = RSVGLogo()
        logo_data = self.data
        logo.path = logo_data['path']
        logo.x = logo_data['x']
        logo.y = logo_data['y']
        size = Size()
        size.width = logo_data['size']['width']
        size.height = logo_data['size']['height']
        logo.size = size
        return logo


class LogoForm(Form):
    path = StringField('Path:', validators=[])
    x = IntegerField('Pos x:', validators=[InputRequired()])
    y = IntegerField('Pos y:', validators=[InputRequired()])
    size = FormField(SizeForm, 'Size:', validators=[])
    alpha = FloatField('Alpha:',
                       validators=[InputRequired(), NumberRange(constants.MIN_ALPHA, constants.MAX_ALPHA)])

    def get_data(self) -> Logo:
        logo = Logo()
        logo_data = self.data
        logo.path = logo_data['path']
        logo.x = logo_data['x']
        logo.y = logo_data['y']
        size = Size()
        size.width = logo_data['size']['width']
        size.height = logo_data['size']['height']
        logo.size = size
        logo.alpha = logo_data['alpha']
        return logo


class RationalForm(Form):
    num = IntegerField('Numerator:', validators=[InputRequired()])
    den = IntegerField('Denominator:', validators=[InputRequired()])

    def get_data(self) -> Rational:
        ratio = Rational()
        ratio_data = self.data
        ratio.num = ratio_data['num']
        ratio.den = ratio_data['den']
        return ratio


class HostAndPortForm(Form):
    host = StringField('Host:', validators=[InputRequired()])
    port = IntegerField('Port:', validators=[InputRequired()])

    def get_data(self) -> HostAndPort:
        host = HostAndPort()
        host_data = self.data
        host.host = host_data['host']
        host.port = host_data['port']
        return host


class TagListField(Field):
    widget = TextInput()

    def _value(self):
        """values on load"""
        if self.data:
            return u', '.join(self.data)
        else:
            return u''

    def process_formdata(self, valuelist):
        if valuelist:
            self.data = [x.strip() for x in valuelist[0].split(',')]
        else:
            self.data = []
