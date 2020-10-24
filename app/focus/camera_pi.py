import io
import time
import picamera
from .base_camera import BaseCamera
#from phototron.rpimodule import RpiModule
from ivport_v2 import ivport

class Camera(BaseCamera):
    def __init__(self, cam_id):
        BaseCamera.__init__(self, cam_id)
    
    @staticmethod
    def frames(cam_id):
        print("frames called from %s on cam %s"% (__class__, cam_id))
        iv = ivport.IVPort(ivport.TYPE_QUAD2)
        
        print("change to cam %s" % cam_id)
        iv.camera_change(cam_id)

        with picamera.PiCamera() as camera:
            # let camera warm up
            time.sleep(0)

            stream = io.BytesIO()
            for foo in camera.capture_continuous(stream, 'jpeg',
                                                 use_video_port=True):
                # return current frame
                stream.seek(0)
                yield stream.read()

                # reset stream for next frame
                stream.seek(0)
                stream.truncate()
