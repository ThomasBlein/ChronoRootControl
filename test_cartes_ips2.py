#!/usr/bin/env python

import os
from ivport_v2 import  ivport
import time

def still_capture():
    # raspistill capture
    def capture(camera):
        "This system command for raspistill capture"
        cmd = "raspistill -t 2 -e png --exif Exif.Image.ProcessingSoftware=raspistill -o still_CAM%d.png" % camera
        os.system(cmd)

    iv = ivport.IVPort(ivport.TYPE_QUAD2, iv_jumper='A')
    for cam in [1, 2, 3, 4]:
        iv.camera_change(cam)
        capture(cam)
    iv.close()

still_capture()