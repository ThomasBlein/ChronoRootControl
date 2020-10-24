"""
The running configuration that is based on default settings
"""
import os

onRPi = True if os.uname().machine[:3] == 'arm' else False

if onRPi:
    from default_config import Config
else:
    from laptop_config import Config

Config.onRPi = onRPi

Config.SITE_NAME = "ChronoRoot Module Controler"

APP_ROOT = os.path.dirname(os.path.realpath(__file__))

Config.LOGFILE = os.path.join(
                    APP_ROOT,
                    'log/%s.log' % Config.SITE_NAME.replace(' ', '_')
                    )

Config.SHDL_LOG_FILE = os.path.join(
                        APP_ROOT,
                        'log/%s_SHDL.log' % Config.SITE_NAME.replace(' ', '_')
                    )

Config.MULE_NO = 1
