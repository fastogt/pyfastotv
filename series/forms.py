from flask_wtf import FlaskForm
from pyfastocloud_models.series.entry import Serial
from wtforms.fields import StringField, SubmitField, BooleanField, IntegerField
from wtforms.validators import InputRequired, NumberRange


class SerialForm(FlaskForm):
    name = StringField('Name:', validators=[InputRequired()])
    group = StringField('Group:', validators=[])
    description = StringField('Description:', validators=[])
    season = IntegerField('Season:', validators=[InputRequired(), NumberRange(min=0)])
    visible = BooleanField('Visible for clients:', validators=[])
    submit = SubmitField('Apply')

    def make_entry(self):
        return self.update_entry(Serial())

    def update_entry(self, serial: Serial):
        serial.name = self.name.data
        serial.group = self.group.data
        serial.description = self.description.data
        serial.season = self.season.data
        serial.visible = self.visible.data
        return serial
