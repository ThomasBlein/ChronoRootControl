"""
The forms used in the application

AppSettingsForm: Global Application Settings
"""

import datetime

from flask_wtf import FlaskForm as Form

from wtforms import (BooleanField, IntegerField, SelectMultipleField,
                     TextAreaField, ValidationError)
from wtforms.ext.dateutil.fields import DateTimeField
from wtforms.validators import Optional

class AppSettingsForm(Form):
    """
    Settings of an experiemnt
    """
    systemDate = DateTimeField("date", display_format='%Y-%m-%d %H:%M:%S %z',
                        default=datetime.datetime.now)


class BackLightForm(Form):
    """
    Switch fo the backlighSwitch fo the backlight
    """
    ir = BooleanField("ir",
                      default=True,
                      description="Turn the infrared lights on/off")
