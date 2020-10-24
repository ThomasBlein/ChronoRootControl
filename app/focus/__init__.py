"""
Live preview from camera
"""
from ..options.form import BackLightForm
import os
from config import Config
from flask import (Blueprint, abort, flash, redirect, render_template, request,
                   url_for, Response)
from .camera_pi import Camera


from phototron.rpimodule import RpiModule
import time

focus_page = Blueprint('focus_page', __name__,
                       template_folder='templates',
                       static_folder='static')

@focus_page.route('/<int:cam_id>', methods=['GET', 'POST'])
def index(cam_id):
    """Video streaming home page."""
    rpi = RpiModule()
    light = rpi.light
    backlight_form = BackLightForm(ir=light.state, prefix="backlight")
    if backlight_form.validate_on_submit() and backlight_form.data:
        if backlight_form.data['ir']:
            light.state = light.ON
        else:
            light.state = light.OFF

    return render_template('focus.html', cam_id=cam_id,
            light_state=light.state,
            backlight_form=backlight_form)

def gen(camera):
    """Video streaming generator function."""
    print("gen : camera %s (%s)" % (camera.cam_id, camera))
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        time.sleep(1)


@focus_page.route('/video_feed/<int:cam_id>')
def video_feed(cam_id):
    """Video streaming route. Put this in the src attribute of an img tag."""
    print("video_feed feed called for camera %s"%cam_id)
    return Response(gen(Camera(cam_id=cam_id)),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
