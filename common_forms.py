import pyfastocloud_models.constants as constants
from pyfastocloud_models.common_entries import Rational, Size, Logo, RSVGLogo, HostAndPort, HttpProxy, Point, InputUrl, \
    OutputUrl
from wtforms import Form
from wtforms.fields import StringField, IntegerField, FormField, FloatField, SelectField, BooleanField, Field
from wtforms.validators import InputRequired, Length, NumberRange, Optional
from wtforms.widgets import TextInput


class UrlForm(Form):
    id = IntegerField('Id:', validators=[InputRequired()], render_kw={'readonly': 'true'})
    uri = StringField('Url:', validators=[InputRequired(),
                                          Length(min=constants.MIN_URI_LENGTH, max=constants.MAX_URI_LENGTH)])


class HttpProxyForm(Form):
    uri = StringField('Url:', validators=[])
    user = StringField('User:', validators=[])
    password = StringField('Password:', validators=[])

    def get_data(self) -> HttpProxy:
        proxy = HttpProxy()
        proxy_data = self.data
        proxy.uri = proxy_data[HttpProxy.URI_FIELD]
        proxy.user = proxy_data[HttpProxy.USER_FIELD]
        proxy.password = proxy_data[HttpProxy.PASSWORD_FIELD]
        return proxy


class InputUrlForm(UrlForm):
    AVAILABLE_USER_AGENTS = [(constants.UserAgent.GSTREAMER, 'GStreamer'), (constants.UserAgent.VLC, 'VLC'),
                             (constants.UserAgent.FFMPEG, 'FFmpeg'), (constants.UserAgent.WINK, 'Wink'),
                             (constants.UserAgent.CHROME, 'Chrome'), (constants.UserAgent.MOZILLA, 'Mozilla'),
                             (constants.UserAgent.SAFARI, 'Safari')]

    user_agent = SelectField('User agent:', validators=[], choices=AVAILABLE_USER_AGENTS,
                             coerce=constants.UserAgent.coerce)
    stream_link = BooleanField('SteamLink:', validators=[])
    proxy = FormField(HttpProxyForm, 'Http proxy:', validators=[])
    program_number = IntegerField('Program number:', validators=[Optional()])
    multicast_iface = StringField('Multicast iface:', validators=[])

    def get_data(self) -> InputUrl:
        url = InputUrl()
        proxy_data = self.data
        url.id = proxy_data[InputUrl.ID_FIELD]
        url.uri = proxy_data[InputUrl.URI_FIELD]
        if InputUrl.MULTICAST_IFACE_FIELD in proxy_data:
            if proxy_data[InputUrl.MULTICAST_IFACE_FIELD]:
                url.multicast_iface = proxy_data[InputUrl.MULTICAST_IFACE_FIELD]
        if InputUrl.PROGRAM_NUMBER_FIELD in proxy_data:
            if proxy_data[InputUrl.PROGRAM_NUMBER_FIELD]:
                url.program_number = proxy_data[InputUrl.PROGRAM_NUMBER_FIELD]
        if InputUrl.PROXY_FIELD in proxy_data:
            if proxy_data[InputUrl.PROXY_FIELD][HttpProxy.URI_FIELD]:
                url.proxy = HttpProxy.make_entry(proxy_data[InputUrl.PROXY_FIELD])
        if InputUrl.STREAM_LINK_FIELD in proxy_data:
            url.stream_link = proxy_data[InputUrl.STREAM_LINK_FIELD]
        return url


class OutputUrlForm(UrlForm):
    AVAILABLE_HLS_TYPES = [(constants.HlsType.HLS_PULL, 'PULL'), (constants.HlsType.HLS_PUSH, 'PUSH')]

    http_root = StringField('Http root:', validators=[], render_kw={'readonly': 'true'})
    hls_type = SelectField('HLS Type:', validators=[], choices=AVAILABLE_HLS_TYPES, coerce=constants.HlsType.coerce)

    def get_data(self) -> OutputUrl:
        url = OutputUrl()
        proxy_data = self.data
        url.id = proxy_data[OutputUrl.ID_FIELD]
        url.uri = proxy_data[OutputUrl.URI_FIELD]
        if OutputUrl.HTTP_ROOT_FIELD in proxy_data:
            if proxy_data[OutputUrl.HTTP_ROOT_FIELD]:
                url.http_root = proxy_data[OutputUrl.HTTP_ROOT_FIELD]

        if OutputUrl.HLS_TYPE_FIELD in proxy_data:
            url.hls_type = proxy_data[OutputUrl.HLS_TYPE_FIELD]
        return url


class SizeForm(Form):
    width = IntegerField('Width:', validators=[])
    height = IntegerField('Height:', validators=[])

    def get_data(self) -> Size:
        size = Size()
        size_data = self.data
        size.width = size_data['width']
        size.height = size_data['height']
        return size


class PointForm(Form):
    x = IntegerField('X:', validators=[])
    y = IntegerField('Y:', validators=[])

    def get_data(self) -> Point:
        point = Point()
        point_data = self.data
        point.x = point_data['x']
        point.y = point_data['y']
        return point


class RSVGLogoForm(Form):
    path = StringField('Path:', validators=[])
    position = FormField(PointForm, 'Position:', validators=[])
    size = FormField(SizeForm, 'Size:', validators=[])

    def get_data(self) -> RSVGLogo:
        logo = RSVGLogo()
        logo_data = self.data
        logo.path = logo_data['path']
        logo.position = logo_data['position']
        size = logo_data['size']
        logo.size = size
        return logo


class LogoForm(Form):
    path = StringField('Path:', validators=[])
    position = FormField(PointForm, 'Position:', validators=[])
    size = FormField(SizeForm, 'Size:', validators=[])
    alpha = FloatField('Alpha:', validators=[InputRequired(), NumberRange(Logo.MIN_LOGO_ALPHA, Logo.MAX_LOGO_ALPHA)])

    def get_data(self) -> Logo:
        logo = Logo()
        logo_data = self.data
        logo.path = logo_data['path']
        logo.position = logo_data['position']
        size = logo_data['size']
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
