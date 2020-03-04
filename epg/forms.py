from os.path import splitext
from flask_wtf import FlaskForm

from wtforms.fields import StringField, SubmitField, FileField
from wtforms.validators import InputRequired, Length

from pyfastocloud_models.epg.entry import Epg

import pyfastocloud_models.constants as constants


def splitext_(path):
    for ext in ['.tar.gz', '.tar.bz2']:
        if path.endswith(ext):
            return path[:-len(ext)], path[-len(ext):]
    return splitext(path)


def gen_extension(uri: str) -> str:
    file_name, ext = splitext_(uri)
    if not ext:
        ext = '.xml'
    return ext


class EpgForm(FlaskForm):
    uri = StringField('Url:', validators=[InputRequired(),
                                          Length(min=constants.MIN_URL_LENGTH, max=constants.MAX_URL_LENGTH)])
    extension = StringField('Extension:', validators=[])
    apply = SubmitField('Apply')

    def make_entry(self) -> Epg:
        return self.update_entry(Epg())

    def update_entry(self, entry: Epg) -> Epg:
        entry.uri = self.uri.data
        if self.extension.data:
            entry.extension = self.extension.data
        else:
            entry.extension = gen_extension(entry.uri)
        return entry


class UploadEpgForm(FlaskForm):
    file = FileField()
    submit = SubmitField('Upload')
