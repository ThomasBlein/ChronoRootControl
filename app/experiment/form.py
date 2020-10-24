"""
The forms used in the application

SettingsForm: Settings of an experiment
"""
import datetime

from flask_wtf import FlaskForm as Form
from wtforms import (BooleanField, IntegerField, SelectMultipleField,
                     TextAreaField, ValidationError)
from wtforms.ext.dateutil.fields import DateTimeField
from wtforms.validators import Optional
from config import Config

from phototron.rpimodule import RpiModule

class SettingsForm(Form):
    """
    Settings of an experiemnt
    """

    rpi = RpiModule()

    desc = TextAreaField(u"Description:",
                        validators=[Optional()],
                        description='about this experience')
    start = DateTimeField("start",
                          display_format='%Y-%m-%d %H:%M:%S %z',
                          default=datetime.datetime.now)
    end = DateTimeField("end",
                        display_format='%Y-%m-%d %H:%M:%S %z',
                        default=datetime.datetime.now)
    interval = IntegerField("interval",
                            default=360,
                            description= 'Interval (in minutes)')
    ir = BooleanField("ir",
                      default=True,
                      description="Turn the infrared lights on/off")



    cameras = SelectMultipleField('cameras',
                                  choices= [(cam,"Camera%s"%cam) for cam in Config.CAMS],
                                  default=[1],
                                  coerce=int,
                                  description= 'Cameras to use')
    camera = rpi.selector.get_camera()

    def validate_cameras(form, field):
        """
        validate function for the choice of cameras

        At list one camera should be selected

        Args:
          form : Form
            The form to check
          field : Field
            The field to check
        """
        if len(field.data) < 1:
            raise ValidationError("Select at least one camera")
        #TODO: add min time validation : 1 photo par min max
