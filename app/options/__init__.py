##
# Configuration management
#

from .form import AppSettingsForm, BackLightForm
from .settings_manager import Settings
from datetime import datetime
import subprocess
import os
from time import sleep
from io import BytesIO
from config import Config

from phototron.rpimodule import RpiModule


from flask import (Blueprint, abort, flash, redirect, render_template, request,
                   url_for, Response)

config_page = Blueprint('config_page', __name__,
                            template_folder='templates',
                            static_folder='static')


@config_page.route('/', methods=['GET', 'POST'])
def conf():
    """
    Device settings page
    """
    now = '{0:%Y-%m-%d %H:%M:%S}'.format(datetime.now())
    rpi = RpiModule()
    light = rpi.light

    app_setting_form = AppSettingsForm(prefix="app_setting")
    backlight_form = BackLightForm(ir=light.state, prefix="backlight")

    if app_setting_form.validate_on_submit() and app_setting_form.data:
        retval = setSystemTime(app_setting_form.data['systemDate'], network=False)

        if retval == 0:
            flash('System date sucessfuly changed : %s'%app_setting_form.data)
        else:
            flash('Error : Date change failed. System said : %s'%retval)

    if backlight_form.validate_on_submit() and backlight_form.data:
        if backlight_form.data['ir']:
            light.state = light.ON
        else:
            light.state = light.OFF

    return render_template('config.html', date=now,
            app_setting_form=app_setting_form,
            backlight_form=backlight_form,
            light_state=light.state, config=Config)

def setSystemTime(mydate, network=True):
    """ Set System system time
          * manually
          * or request time from ntpd server
    """
    if network:
        pass
    else:
        datestring = '{0:%Y-%m-%d %H:%M:%S}'.format(mydate)
        p = subprocess.Popen('date -s "%s"'%datestring, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        output = b""
        for line in p.stdout.readlines():
            output += line
        retval = p.wait()
        if retval == 0:
            return retval
        else:
            return output.decode('UTF8')
