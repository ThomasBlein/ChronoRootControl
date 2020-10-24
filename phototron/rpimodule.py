#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Created on 26 févr. 2018

@author: Vladimir Daric
@email: vladimir.daric@cnrs.fr

ChronoRoot robot module implementation

RpiModule class impements all ChronoRoot robot functions

'''

import logging
import os
import time, arrow
from config import Config
from phototron.camera_selector import SelectorFactory
from phototron.light import Light
from app.experiment.models import Experiment
from filelock import FileLock, Timeout

class RpiModule(object):
    """Toplevel class
       Implements all ChronoRoot robot functions and manages
       configuration and initialisation of all components

       This class has only one static method. The take_picture method
       all the complexity is delegated to subclasses and sub-modules.
    """
    Count = 0   # This represents the count of objects of this class
    def __init__(self):
        """Init - get the selector type from the configuration file and
        init the selector, init the logger, init the file lock

        file lock is used to prevent simultaneous acces to camera
        """

        selector_type = Config.SELECTOR_TYPE
        self.selector  = SelectorFactory.createSelector(selector_type)
        self.light = Light()
        self.logger = self.logger()
        self.logger.debug("RpiModule object initialized")
        self.lock = FileLock(Config.LOCK_FILE, Config.LOCK_TIMEOUT)
        RpiModule.Count += 1

    def __del__(self):
        """properly remove RpiModule object instances
        """

        self.logger.debug('deleting : %s'%(self))
        RpiModule.Count -= 1
        if RpiModule.Count == 0:
            self.logger.debug('Last RpiModule object deleted')
        else:
            self.logger.debug('%s RpiModule objects remaining ' % RpiModule.Count)
        del self.selector
        del self


    def logger(self):
        """Logger initialisation
        """

        logger = logging.getLogger(__name__)
        return logger

    @staticmethod
    def take_picture(xpid):
        """
        Take the picture.

        static method, only needs the experiment ID, parameters are stored in experiment
        description json file

        :param xpid: Ecperiment ID
        :type event: string

        :returns: boolean
        :rtype: boolean
        """

        rpi = RpiModule()
        rpi.logger.info('taking picture for task : %s. RpiModule obj ref : %s'%(xpid, rpi))
        light = rpi.light
        exp = Experiment(directory=os.path.join(Config.WORKING_DIR, xpid))

        cameras = exp.cameras
        params = exp.img_params

        #test the multiplexer
        if not rpi.selector.self_check():
            rpi.logger.error('Multiplexer failure')
            #put info in json file ..
            exp.state = "FAILED"
            exp.message = "Multiplexer error fatal error"
            exp.dump()
            return False

        #camera is used -> Experiment in progress ?
        ## wait a while ...
        retries = 0
        while retries < Config.CAM_RETRIES:
            retries += 1
            try:
                with rpi.lock.acquire():
                    rpi.logger.info('lock acquired')
                    #TURN THE LIGHTS
                    if exp.ir:
                        rpi.logger.info('turning lights ON')
                        light.state = Light.ON
                    else:
                        rpi.logger.info('turning lights OFF')
                        light.state = Light.OFF

                    rpi.logger.info('rpimodule requested cams list : %s' % cameras)

                    step = []
                    for camera in cameras:
                        rpi.logger.debug('Started image capture on cam %s.' % camera)
                        if camera in Config.CAMS:
                            instant_date = arrow.now().format('YYYY-MM-DD_HH-mm-ss')
                            #create cam folder & add cam_folder path to imagepath
                            camdir = os.path.join(exp.workdir, "%s"%camera)
                            rpi.logger.debug('# # # # # # new path %s'%camdir)
                            if not os.path.isdir(camdir):
                                os.mkdir(camdir)

                            imagepath = os.path.join(camdir, '%s_%s.png' % (instant_date, camera))
                            ##CAPTURE IMAGE
                            if rpi.selector.capture(camera, imagepath, params):
                                step.append((instant_date, camera, imagepath))
                            else:
                                exp.message = "Camera %s was buissy. Skipped step" % camera
                        else:
                            rpi.logger.info('Requested camera (%s) is not present in config file. Please check config.py file.'%(camera))

                    if light.state:
                        rpi.logger.info('turning lights OFF')
                        light.state = Light.OFF
                    if len(step) > 0:
                        exp.new_step(tuple(step))
                        exp.message = "OK"
                    exp.dump()
                    return True
            except Timeout:
                print("Another instance of this application currently holds the lock.")
            finally:
                if rpi.lock.is_locked:
                    rpi.lock.release()
                    rpi.logger.info('lock release forced')
                rpi.logger.info('lock is now free for other experiments')
        rpi.logger.error('Could not acquire cameras after %s retries.'%Config.CAM_RETRIES)
        return False
