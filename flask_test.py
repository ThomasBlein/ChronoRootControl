# -*- coding: utf-8 -*-
## to run thos test
##    source bin/activate
##  > python flask_test.py
import os
from flask import Flask
#import flaskr
from app.experiment.models import Experiment
import unittest
import uuid
import tempfile
# from flask import g
from apscheduler.schedulers.background import BackgroundScheduler
import arrow

class TestExperimentMethods(unittest.TestCase):

    def setUp(self):
        self.app = Flask(__name__)
        #expid = str(uuid.uuid1())
        now = arrow.now()

        _scheduler = getattr(self.app, 'scheduler', None)
        if _scheduler is None:
            _scheduler = BackgroundScheduler()
            self.app.scheduler = _scheduler
        if not _scheduler.running:
            _scheduler.start()

        self.tmpfolder = tempfile.mkdtemp()
        exp = { "desc" : "Fake test XP",
                "status": "Setup",
                "ir": False,
                "cameras":  [1,2,3,4],
                "message": 'msg',
                }
        self.newExp = Experiment(app=self.app)
        self.newExp.from_dict(exp)
        self.newExp.workdir = os.path.join(self.tmpfolder, self.newExp.xp_id())

    def tearDown(self):
        import shutil
        shutil.rmtree(self.tmpfolder)


    def test_dump_and_load(self):
        """Dump an XP, load it. The two has to be equal
        """

        self.newExp.dump()
        otherExp = Experiment(app=self.app, directory=self.newExp.workdir)
        import shutil
        shutil.rmtree(otherExp.workdir)
        self.assertEqual(self.newExp, otherExp)

    def test_time_point_setter(self):
        """
        """
        somepath = "/tmp/%s"%self.newExp.expid
        self.newExp.new_step(4, somepath)
        #print(self.newExp.to_dict())
        self.assertEqual((4,                       somepath,                1),
                         (self.newExp.steps[0][1], self.newExp.steps[0][2], self.newExp.steps_nb))

    def test_insert_in_scheduler(self):
        inserted = False
        now =  arrow.now()
        self.newExp.start = now.format('YYYY-MM-DD HH:mm:ssZ')
        self.newExp.interval = 5
        self.newExp.end = now.shift(hours=+1).format('YYYY-MM-DD HH:mm:ssZ')

        jobid = self.newExp.insert_in_scheduler()
        myjob = self.app.scheduler.get_job(jobid)
        next_run_time =  myjob.next_run_time
        if next_run_time is not None and self.newExp.expid == myjob.id:
            inserted = True

        self.assertTrue(inserted)

    def test_remove_from_scheduler(self):
        """Insert a job in schendular and remove it
        """
        now =  arrow.now()
        wasin = False
        self.newExp.start = now.format('YYYY-MM-DD HH:mm:ssZ')
        self.newExp.interval = 5
        self.newExp.end = now.shift(hours=+1).format('YYYY-MM-DD HH:mm:ssZ')

        jobid = self.newExp.insert_in_scheduler()
        myjob = self.app.scheduler.get_job(jobid)

        if myjob.id in (job.id for job in self.app.scheduler.get_jobs()):
            wasin = True

        self.newExp.remove_from_scheduler()

        if myjob.id in (job.id for job in self.app.scheduler.get_jobs()):
            stillin = True
        else:
            stillin = False

        self.assertTrue(wasin and not stillin)

    def test_delete(self):
        """Test XP files remooval
        """
        deleted = False
        hadworkdir = False
        self.newExp.dump()
        if os.path.exists(self.newExp.workdir):
            hadworkdir = True

        self.newExp.delete()

        if not os.path.exists(self.newExp.workdir):
            deleted = True

        self.assertTrue(hadworkdir and deleted)



if __name__ == '__main__':
    unittest.main()
