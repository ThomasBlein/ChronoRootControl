"""
The default configuration settings
"""
import os

class Config(object):
    DEBUG = False
    WORKING_DIR = os.path.join(
                    os.path.dirname(os.path.realpath(__file__)),
                    'app/test/experiences/')


    SELECTOR_PRESENT = False # IV PORT MODULE PRESENCE

    SELECTOR_TYPE = "NullSelector" #possible values : TYPE_QUAD, TYPE_QUAD2, TYPE_DUAL, TYPE_DUAL2

    CAMS = (1,)         # CAMERAS PRESENCE & DISPOSITION
                        # possible values:
                        # One cam :  (1, ), (2, ), (3, ), (4, )
                        # Two cams : (1,2),(1,3),(1,4),(2,3),(2,4)
                        # Three cams : (1,2,3),(1,2,4),(2,3,4)
                        # Four cams : (1,2,3,4)
                        # the order inside the list is not important
    CAM_WARMUP = 1
    STREAM_RESOLUTION = (1640, 1232)
    IR_GPIO = 32
