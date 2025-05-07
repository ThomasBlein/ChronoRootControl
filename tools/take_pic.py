#!/usr/bin/env python

import os
import time
from optparse import OptionParser

from ivport_v2 import ivport


def still_capture():
    # raspistill capture
    def capture(camera):
        "This system command for raspistill capture"
        cmd = "raspistill -t 10 -o still_CAM%d.jpg" % camera
        os.system(cmd)

    iv = ivport.IVPort(ivport.TYPE_QUAD2, iv_jumper='A')
    iv.camera_change(1)
    capture(1)
    iv.camera_change(2)
    capture(2)
    iv.close()




# main capture examples
# all of them are functional
def main():
    usage = "usage: %prog [options] arg"
    parser = OptionParser(usage)
    parser.add_option("-o", "--out", dest="filename", default="still_CAM",
                      help="save image to FILE")
    parser.add_option("-e", "--encoding", dest="encoding", default="png",
                      help="Encoding to use for output file (jpg, bmp, gif, png [default])")
    parser.add_option("-c", "--camera", dest="camera", default=1,
                      help="camera selection (single number : 1 to 4 or comma separated list)")
    
    
    
    (options, args) = parser.parse_args()
    
        # raspistill capture
    def capture(filename="still_CAM", encoding="png"):
        "This system command for raspistill capture"
        cmd = "raspistill -n -e %s -o %s.%s" % (encoding, filename, encoding)
        os.system(cmd)
    
    if type(options.camera) is str and len(options.camera) > 1:
        ## several cams
        cameras = options.camera.split(",")
        cameras = [int(elem) for elem in cameras if int(elem) in range(5)]
        if len(cameras) == 0:
            print("Camera option is a comma separated list of numbers. Exemple :./take_pic.py -c 1,2 ....")
            sys.exit(1)
    else:
        ## one cam
        camera = int(options.camera)
        if camera in range(5):
            cameras = [camera, ]
        else:
            print("Camera option must be a number.  Exemple :./take_pic.py -c 1,2 ....")
            sys.exit(1)
            
            
    for cam in cameras:
        iv = ivport.IVPort(ivport.TYPE_QUAD2, iv_jumper='A')
        iv.camera_change(cam)
        capture(filename=options.filename, encoding=options.encoding)
    
    return
    
    
    
    
    
    
    
    
    

if __name__ == "__main__":
    main()
    sys.exit(1)
