import pyfastocloud_models.constants as constants
from flask_wtf import FlaskForm
from pyfastocloud_models.stream.entry import IStream, HardwareStream, ProxyStream, RelayStream, EncodeStream, \
    TimeshiftRecorderStream, CatchupStream, TimeshiftPlayerStream, TestLifeStream, VodRelayStream, VodEncodeStream, \
    ProxyVodStream, CodRelayStream, CodEncodeStream, StreamLogLevel, EventStream
from wtforms.fields import StringField, SubmitField, SelectField, IntegerField, FormField, BooleanField, FloatField, \
    DateTimeField, FieldList
from wtforms.validators import InputRequired, Length, NumberRange, Optional

from app.common.common_forms import SizeForm, LogoForm, RationalForm, RSVGLogoForm, OutputUrlForm, InputUrlForm


class TagListField(StringField):
    """Stringfield for a list of separated tags"""

    def __init__(self, label='', validators=None, remove_duplicates=True, to_lowercase=False, separator=' ', **kwargs):
        """
        Construct a new field.
        :param label: The label of the field.
        :param validators: A sequence of validators to call when validate is called.
        :param remove_duplicates: Remove duplicates in a case insensitive manner.
        :param to_lowercase: Cast all values to lowercase.
        :param separator: The separator that splits the individual tags.
        """
        super(TagListField, self).__init__(label, validators, **kwargs)
        self.remove_duplicates = remove_duplicates
        self.to_lowercase = to_lowercase
        self.separator = separator
        self.data = []

    def _value(self):
        if self.data:
            return u', '.join(self.data)
        else:
            return u''

    def process_formdata(self, valuelist):
        if valuelist:
            self.data = [x.strip() for x in valuelist[0].split(self.separator)]
            if self.remove_duplicates:
                self.data = list(self._remove_duplicates(self.data))
            if self.to_lowercase:
                self.data = [x.lower() for x in self.data]

    @classmethod
    def _remove_duplicates(cls, seq):
        """Remove duplicates in a case insensitive, but case preserving manner"""
        d = {}
        for item in seq:
            if item == '':
                continue
            if item.lower() not in d:
                d[item.lower()] = True
                yield item


class OptionalFormField(FormField):
    def process(self, formdata, *args, **kwargs):
        self._formdata = formdata
        return super(OptionalFormField, self).process(formdata, *args, **kwargs)

    def validate(self, *args, **kwargs):
        return True


class IStreamForm(FlaskForm):
    name = StringField('Name:', default='Stream',
                       validators=[InputRequired(),
                                   Length(min=constants.MIN_STREAM_NAME_LENGTH, max=constants.MAX_STREAM_NAME_LENGTH)])
    tvg_id = StringField('Epg ID:',
                         validators=[Optional(),
                                     Length(min=constants.MIN_STREAM_TVG_ID_LENGTH,
                                            max=constants.MAX_STREAM_TVG_ID_LENGTH)])
    tvg_name = StringField('Tvg-Name:', validators=[])
    tvg_logo = StringField('Icon:',
                           validators=[Optional(),
                                       Length(min=constants.MIN_URI_LENGTH, max=constants.MAX_URI_LENGTH)])
    groups = TagListField('Groups:', separator=',',
                          validators=[Length(max=8, message='You can only use up to 8 groups.')])
    price = FloatField('Price:',
                       validators=[InputRequired(), NumberRange(constants.MIN_PRICE, constants.MAX_PRICE)])
    visible = BooleanField('Visible for clients:', validators=[])
    iarc = IntegerField('Age Rating:',
                        validators=[InputRequired(), NumberRange(min=constants.MIN_IARC, max=constants.MAX_IARC)])
    view_count = IntegerField('Views count', validators=[InputRequired(), NumberRange(min=0)],
                              render_kw={'readonly': 'true'})
    output = FieldList(FormField(OutputUrlForm), 'Output:')
    submit = SubmitField('Confirm')

    def make_entry(self) -> IStream:
        return self.update_entry(IStream())

    def update_entry(self, entry: IStream) -> IStream:
        entry.name = self.name.data
        if self.tvg_id.data:
            entry.tvg_id = self.tvg_id.data
        else:
            entry.tvg_id = None

        if self.tvg_name.data:
            entry.tvg_name = self.tvg_name.data
        else:
            entry.tvg_name = None

        entry.tvg_logo = self.tvg_logo.data
        entry.groups = self.groups.data

        entry.price = self.price.data
        entry.visible = self.visible.data
        entry.iarc = self.iarc.data
        entry.view_count = self.view_count.data
        outputs = []
        for inp in self.output:
            outputs.append(inp.get_data())
        entry.output = outputs
        entry.meta = []
        # for entry in self.extra_config_fields.entries:
        # entry.extra_config_fields = self.extra_config_fields.get_data()
        return entry


class ProxyStreamForm(IStreamForm):
    def make_entry(self):
        return self.update_entry(ProxyStream())

    def update_entry(self, entry: ProxyStream):
        return super(ProxyStreamForm, self).update_entry(entry)


class HardwareStreamForm(IStreamForm):
    AVAILABLE_LOG_LEVELS_PAIRS = [(StreamLogLevel.LOG_LEVEL_EMERG, 'EVERG'), (StreamLogLevel.LOG_LEVEL_ALERT, 'ALERT'),
                                  (StreamLogLevel.LOG_LEVEL_CRIT, 'CRITICAL'),
                                  (StreamLogLevel.LOG_LEVEL_ERR, 'ERROR'),
                                  (StreamLogLevel.LOG_LEVEL_WARNING, 'WARNING'),
                                  (StreamLogLevel.LOG_LEVEL_NOTICE, 'NOTICE'),
                                  (StreamLogLevel.LOG_LEVEL_INFO, 'INFO'),
                                  (StreamLogLevel.LOG_LEVEL_DEBUG, 'DEBUG')]

    input = FieldList(FormField(InputUrlForm), 'Input:')
    log_level = SelectField('Log level:', validators=[], choices=AVAILABLE_LOG_LEVELS_PAIRS,
                            coerce=StreamLogLevel.coerce)
    audio_select = IntegerField('Audio select:',
                                validators=[Optional(), NumberRange(constants.MIN_AUDIO_CHANNELS_COUNT,
                                                                    constants.MAX_AUDIO_CHANNELS_COUNT)])
    have_video = BooleanField('Have video:', validators=[])
    have_audio = BooleanField('Have audio:', validators=[])
    loop = BooleanField('Loop:', validators=[])
    restart_attempts = IntegerField('Max restart attempts and frozen:',
                                    validators=[NumberRange(1, 1000)])
    auto_exit_time = IntegerField('Auto exit time:', validators=[Optional()])
    extra_config_fields = StringField('Extra config args:', validators=[])

    def make_entry(self):
        return self.update_entry(HardwareStream())

    def update_entry(self, entry: HardwareStream):
        inputs = []
        for inp in self.input:
            inputs.append(inp.get_data())
        entry.input = inputs

        if self.audio_select.data is not None:
            entry.audio_select = self.audio_select.data

        entry.have_video = self.have_video.data
        entry.have_audio = self.have_audio.data
        entry.log_level = self.log_level.data
        entry.loop = self.loop.data
        entry.restart_attempts = self.restart_attempts.data
        if self.auto_exit_time.data is not None:
            entry.auto_exit_time = self.auto_exit_time.data
        entry.extra_config_fields = self.extra_config_fields.data
        return super(HardwareStreamForm, self).update_entry(entry)


class RelayStreamForm(HardwareStreamForm):
    video_parser = SelectField('Video parser:', validators=[],
                               choices=constants.AVAILABLE_VIDEO_PARSERS)
    audio_parser = SelectField('Audio parser:', validators=[],
                               choices=constants.AVAILABLE_AUDIO_PARSERS)

    def make_entry(self):
        return self.update_entry(RelayStream())

    def update_entry(self, entry: RelayStream):
        entry.video_parser = self.video_parser.data
        entry.audio_parser = self.audio_parser.data
        return super(RelayStreamForm, self).update_entry(entry)


class EncodeStreamForm(HardwareStreamForm):
    relay_video = BooleanField('Relay video:', validators=[])
    relay_audio = BooleanField('Relay audio:', validators=[])
    deinterlace = BooleanField('Deinterlace:', validators=[])
    frame_rate = IntegerField('Frame rate:',
                              validators=[Optional(),
                                          NumberRange(constants.MIN_FRAME_RATE, constants.MAX_FRAME_RATE)])
    volume = FloatField('Volume:',
                        validators=[InputRequired(), NumberRange(constants.MIN_VOLUME, constants.MAX_VOLUME)])
    video_codec = SelectField('Video codec:', validators=[],
                              choices=constants.AVAILABLE_VIDEO_CODECS)
    audio_codec = SelectField('Audio codec:', validators=[],
                              choices=constants.AVAILABLE_AUDIO_CODECS)
    audio_channels_count = IntegerField('Audio channels count:',
                                        validators=[Optional(), NumberRange(constants.MIN_AUDIO_CHANNELS_COUNT,
                                                                            constants.MAX_AUDIO_CHANNELS_COUNT)])
    size = OptionalFormField(SizeForm, 'Size:', validators=[])
    video_bit_rate = IntegerField('Video bit rate:', validators=[Optional()])
    audio_bit_rate = IntegerField('Audio bit rate:', validators=[Optional()])
    logo = OptionalFormField(LogoForm, 'Logo:', validators=[])
    rsvg_logo = OptionalFormField(RSVGLogoForm, 'RSVG Logo:', validators=[])
    aspect_ratio = OptionalFormField(RationalForm, 'Aspect ratio:', validators=[])

    def make_entry(self):
        return self.update_entry(EncodeStream())

    def update_entry(self, entry: EncodeStream):
        entry.relay_video = self.relay_video.data
        entry.relay_audio = self.relay_audio.data
        entry.deinterlace = self.deinterlace.data
        if self.frame_rate.data is not None:
            entry.frame_rate = self.frame_rate.data
        entry.volume = self.volume.data
        entry.video_codec = self.video_codec.data
        entry.audio_codec = self.audio_codec.data
        if self.audio_channels_count.data is not None:
            entry.audio_channels_count = self.audio_channels_count.data
        size = self.size.get_data()
        if size.is_valid():
            entry.size = size
        if self.video_bit_rate.data is not None:
            entry.video_bit_rate = self.video_bit_rate.data
        if self.audio_bit_rate.data is not None:
            entry.audio_bit_rate = self.audio_bit_rate.data
        logo = self.logo.get_data()
        if logo.is_valid():
            entry.logo = logo
        rsvg_logo = self.rsvg_logo.get_data()
        if rsvg_logo.is_valid():
            entry.rsvg_logo = rsvg_logo
        aspect_ratio = self.aspect_ratio.get_data()
        if aspect_ratio.is_valid():
            entry.aspect_ratio = aspect_ratio
        return super(EncodeStreamForm, self).update_entry(entry)


class TimeshiftRecorderStreamForm(RelayStreamForm):
    timeshift_chunk_duration = IntegerField('Chunk duration:',
                                            validators=[InputRequired(),
                                                        NumberRange(constants.MIN_TIMESHIFT_CHUNK_DURATION,
                                                                    constants.MAX_TIMESHIFT_CHUNK_DURATION)])
    timeshift_chunk_life_time = IntegerField('Chunk life time:',
                                             validators=[InputRequired(),
                                                         NumberRange(
                                                             constants.MIN_TIMESHIFT_CHUNK_LIFE_TIME,
                                                             constants.MAX_TIMESHIFT_CHUNK_LIFE_TIME)])

    def make_entry(self):
        return self.update_entry(TimeshiftRecorderStream())

    def update_entry(self, entry: TimeshiftRecorderStream):
        entry.timeshift_chunk_duration = self.timeshift_chunk_duration.data
        entry.timeshift_chunk_life_time = self.timeshift_chunk_life_time.data
        return super(TimeshiftRecorderStreamForm, self).update_entry(entry)


class CatchupStreamForm(TimeshiftRecorderStreamForm):
    start = DateTimeField('Start date:', validators=[InputRequired()])
    stop = DateTimeField('Stop date:', validators=[InputRequired()])

    def make_entry(self):
        return self.update_entry(CatchupStream())

    def update_entry(self, entry: CatchupStream):
        entry.start = self.start.data
        entry.stop = self.stop.data
        return super(CatchupStreamForm, self).update_entry(entry)


class TimeshiftPlayerStreamForm(RelayStreamForm):
    input = FieldList(FormField(InputUrlForm), 'Input:', default=[])
    timeshift_dir = StringField('Chunks directory:', validators=[InputRequired()])
    timeshift_delay = IntegerField('Delay:', validators=[InputRequired(),
                                                         NumberRange(constants.MIN_TIMESHIFT_DELAY,
                                                                     constants.MAX_TIMESHIFT_DELAY)])

    def make_entry(self):
        return self.update_entry(TimeshiftPlayerStream())

    def update_entry(self, entry: TimeshiftPlayerStream):
        entry.timeshift_delay = self.timeshift_delay.data
        entry.timeshift_dir = self.timeshift_dir.data
        return super(TimeshiftPlayerStreamForm, self).update_entry(entry)


class TestLifeStreamForm(RelayStreamForm):
    def make_entry(self):
        return self.update_entry(TestLifeStream())

    def update_entry(self, entry: TestLifeStream):
        return super(TestLifeStreamForm, self).update_entry(entry)


class CodRelayStreamForm(RelayStreamForm):
    def make_entry(self):
        return self.update_entry(CodRelayStream())

    def update_entry(self, entry: CodRelayStream):
        return super(CodRelayStreamForm, self).update_entry(entry)


class CodEncodeStreamForm(EncodeStreamForm):
    def make_entry(self):
        return self.update_entry(CodEncodeStream())

    def update_entry(self, entry: CodEncodeStream):
        return super(CodEncodeStreamForm, self).update_entry(entry)


# VODS

class VodBaseStreamForm(FlaskForm):
    AVAILABLE_VOD_TYPES = [(constants.VodType.VODS, 'VODS'), (constants.VodType.SERIES, 'SERIES')]

    vod_type = SelectField('Vod type:', validators=[InputRequired()], choices=AVAILABLE_VOD_TYPES,
                           coerce=constants.VodType.coerce)

    description = StringField('Description:', validators=[])
    trailer_url = StringField('Trailer URL:',
                              validators=[Optional(),
                                          Length(min=constants.MIN_URI_LENGTH, max=constants.MAX_URI_LENGTH)])
    user_score = FloatField('User score:', validators=[InputRequired(), NumberRange(min=0, max=100)])
    prime_date = DateTimeField('Prime time:', validators=[InputRequired()])
    country = StringField('Country:',
                          validators=[InputRequired(),
                                      Length(min=constants.MIN_COUNTRY_LENGTH, max=constants.MAX_COUNTRY_LENGTH)])
    duration = IntegerField('Duration in (msec):',
                            validators=[InputRequired(), NumberRange(min=0, max=constants.MAX_VIDEO_DURATION_MSEC)])


class ProxyVodStreamForm(ProxyStreamForm, VodBaseStreamForm):
    def make_entry(self):
        return self.update_entry(ProxyVodStream())

    def update_entry(self, entry: ProxyVodStream):
        entry.description = self.description.data
        entry.trailer_url = self.trailer_url.data
        entry.user_score = self.user_score.data
        entry.prime_date = self.prime_date.data
        entry.country = self.country.data
        entry.duration = self.duration.data
        entry.vod_type = self.vod_type.data
        return ProxyStreamForm.update_entry(self, entry)


class VodRelayStreamForm(RelayStreamForm, VodBaseStreamForm):
    def make_entry(self):
        return self.update_entry(VodRelayStream())

    def update_entry(self, entry: VodRelayStream):
        entry.description = self.description.data
        entry.trailer_url = self.trailer_url.data
        entry.user_score = self.user_score.data
        entry.prime_date = self.prime_date.data
        entry.country = self.country.data
        entry.duration = self.duration.data
        entry.vod_type = self.vod_type.data
        return RelayStreamForm.update_entry(self, entry)


class VodEncodeStreamForm(EncodeStreamForm, VodBaseStreamForm):
    def make_entry(self):
        return self.update_entry(VodEncodeStream())

    def update_entry(self, entry: VodEncodeStream):
        entry.description = self.description.data
        entry.trailer_url = self.trailer_url.data
        entry.user_score = self.user_score.data
        entry.prime_date = self.prime_date.data
        entry.country = self.country.data
        entry.duration = self.duration.data
        entry.vod_type = self.vod_type.data
        return EncodeStreamForm.update_entry(self, entry)


class EventStreamForm(VodEncodeStreamForm):
    def __init__(self, *args, **kwargs):
        super(EventStreamForm, self).__init__(*args, **kwargs)
        self.vod_type.validators = []

    def make_entry(self):
        return self.update_entry(EventStream())

    def update_entry(self, entry: EventStream):
        return VodEncodeStreamForm.update_entry(self, entry)
