#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Created on 15 mars 2018
@author: Vladimir Daric

uWisgi mule module


This module is executed by uWisgi mule
it initialises the scheduler and than starts a loop to listen for messages
from the web app
'''
import os
import uwsgi
from phototron.rpimodule import RpiModule
from app.experiment.models import Experiment ### from webapp.models import Experiment
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.executors.pool import ThreadPoolExecutor
from apscheduler.events import *
from datetime import datetime
from flask import json
import arrow
import logging
import pytz
from config import Config

#scheduler initialisation

try:
    scheduler
except NameError:
    scheduler = BackgroundScheduler(executors={'default': ThreadPoolExecutor(1)})

logging.basicConfig(filename=Config.SHDL_LOG_FILE,
                    level=Config.LOG_LEVEL,
                    format=Config.LOG_FORMAT)

log = logging.getLogger(__name__)

handler = logging.FileHandler(Config.SHDL_LOG_FILE, mode='a')
handler.setFormatter(logging.Formatter(Config.LOG_FORMAT))
#handler.setLevel(logging.INFO)
if (log.hasHandlers()):
    log.handlers.clear()
    log.addHandler(handler)

log.info('Director loaded')

if not scheduler.running:
    log.info('Scheduler is not running')
    scheduler.start()
    log.info('Scheduler started: %s'%scheduler.running)
else:
    log.info('Scheduler already started')
    pass

#####
## Callback functions
#      capture scheduler events
def shed_evt_job_executed(event):
    """
    Scheduler event listener callback function,
    triggered by the scheduler on a job execution event

    When called this function updates the experiment status.

    :param event: event object sent by scheduler
    :type event: event

    :returns: None
    :rtype: None
    """

    expid = event.job_id
    exp = Experiment(directory=os.path.join(Config.WORKING_DIR, expid))
    job = scheduler.get_job(expid)
    if job is None:
        exp.status = "ENDED"
        exp.dump()
        return
    exp.next_run_time = "%s" % job.next_run_time
    if job.next_run_time < datetime.now(pytz.timezone('Europe/Paris')):
        exp.status = "ENDED"
    exp.dump()
    return
scheduler.add_listener(shed_evt_job_executed, EVENT_JOB_EXECUTED)

def shed_evt_job_added(event):
    """Scheduler event listener callback function,
    triggered when a job is added to scheduler

    When called this function updates the experiment status.

    :param event: event object sent by scheduler
    :type event: event

    :returns: None
    :rtype: None
    """

    expid = event.job_id
    exp = Experiment(directory=os.path.join(Config.WORKING_DIR, expid))
    job = scheduler.get_job(expid)
    exp.next_run_time = "%s" % job.next_run_time
    exp.status = "RUNNING"
    exp.dump()
    return
scheduler.add_listener(shed_evt_job_added, EVENT_JOB_ADDED)


def shed_evt_job_removed(event):
    """Scheduler event listener callback function,
    triggered when on job removal from scheduler
    (this fonction is normally never called)

    When called this function updates the experiment status.

    :param event: event object sent by scheduler
    :type event: event

    :returns: None
    :rtype: None
    """

    log.info("job removed %s" % event)
    return
scheduler.add_listener(shed_evt_job_removed, EVENT_JOB_REMOVED)

def shed_evt_job_modified(event):
    """Scheduler event listener callback function,
    triggered when a job is modified in scheduler
    (this fonction is normally never called)


    :param event: event object sent by scheduler
    :type event: event

    :returns: None
    :rtype: None
    """

    log.info("job modified %s" % event)
    return
scheduler.add_listener(shed_evt_job_modified, EVENT_JOB_MODIFIED)


def shed_evt_job_error(event):
    """Scheduler event listener callback function,
    triggered when scheduler report job execution error

    When called this function updates the experiment status.

    """

    expid = event.job_id
    exp = Experiment(directory=os.path.join(Config.WORKING_DIR, expid))
    exp.message = "Job execution failed. Error : %s" % event.exception
    exp.dump()
    return
scheduler.add_listener(shed_evt_job_error, EVENT_JOB_ERROR)

def shed_evt_job_missed(event):
    """Callback function,
    triggered when a job is is missed by the scheduler

    :param event: event object sent by scheduler
    :type event: event

    :returns: None
    :rtype: None
    """

    expid = event.job_id
    exp = Experiment(directory=os.path.join(Config.WORKING_DIR, expid))
    exp.message = "Step missed. Error : %s" % event.exception
    #TODO : ajouter des steps vides
    exp.dump()
    return
scheduler.add_listener(shed_evt_job_missed, EVENT_JOB_MISSED)




class ChiefOperator(object):
    """class loaded by the uWisgi mule

    This class implements the mainLoop method.
    When executed in uWisgi mule, this loop lisenen to messages from
    the web app.
    """

    def __init__(self):
        """Init : Logger set-up
        """

        self.logger = self.logger()
        self.logger.info("ChiefOperator object initialized: %s"%self)

    def logger(self):
        """ChiefOperator logger
        """

        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)
        return logger

    @staticmethod
    def mainLoop():
        """loop, listens to webApp messages
        """
        # listen for messages from webapp
        cop = ChiefOperator()
        going_on = True
        while going_on:
            cop.logger.info("ChiefOperator: mainLoop started from %s"%cop)
            try:
                xpid, action = cop.getMessage()
                cop.handle_experiment(xpid, action)
            except Exception as e:
                cop.logger.error("ChiefOperator: somethong gone wrong in the mainLoop: %s"%e)
                going_on = False
                raise e

    def getMessage(self):
        """WebApp message getter

        uses uWsgi message mecanism to recieve messages from the web app

        :returns: expid
        :rtype: string
        :returns: action
        :rtype: string
        """

        while True:
            try:
                message = json.loads(uwsgi.mule_get_msg())
                expid = message['id']
                action = message['action']
                self.logger.info("Got massage: %s, %s"% (expid, action))
            except:
                raise
            if message is not None:
                break
        return expid, action

    def handle_experiment(self, xpid, action):
        """handle the requested action

        :param: expid
        :rtype: string
        :param: action
        :rtype: string
        :returns: None
        :rtype: None
        """

        try:
            {'CREATE': self.create_and_schedule,
            'CANCEL' :self.sched_cancel_xp}[action](xpid)
        except KeyError:
            self.logger.error("Unemplemented action - %s" % action)

        return

    def create_and_schedule(self, xpid):
        """handle experiment creation and schedule

        :param: expid
        :rtype: string
        :returns: None
        :rtype: None
        """

        self.logger.info("create_and_schedule")
        exp = Experiment(directory=os.path.join(Config.WORKING_DIR, xpid))
        exp_id = xpid
        exp.status = "SCHEDULING_IN_PROGRESS"

        ##scheduler accepts loosely converted strings
        start = arrow.get(exp.start).format('YYYY-MM-DD HH:mm:ss').replace('+0000', '')
        end = arrow.get(exp.end).format('YYYY-MM-DD HH:mm:ss').replace('+0000', '')

        job = scheduler.add_job(RpiModule.take_picture, ## PICTURE IT !
                        args=(exp_id,),
                        trigger='interval',
                        start_date=start,
                        end_date=end,
                        minutes=exp.interval,
                        id=exp.expid,
                        replace_existing=True)
        exp.next_run_time = "%s" % job.next_run_time
        self.logger.info("Exp %s scheduled for %s"%(exp.expid, exp.next_run_time))
        scheduler.print_jobs()
        exp.dump()

    def sched_cancel_xp(self, xpid):
        """handle experiment cancelation

        :param: expid
        :rtype: string
        :returns: None
        :rtype: None
        """

        exp = Experiment(directory=os.path.join(Config.WORKING_DIR, xpid))
        self.logger.info("Canceling Exp %s" % xpid )
        exp.status = "Canceled"
        exp.message = "Canceled & removed from scheduler."
        exp.next_run_time = "Never"
        scheduler.remove_job('%s'%(exp.expid))
        exp.dump()

if __name__ == '__main__':
    try:
        ChiefOperator.mainLoop()
    except Exception as e:
        log.error('Exception: %s' % e)
        raise e
