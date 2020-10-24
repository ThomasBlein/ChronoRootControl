"""
Handle the information of all experiments in a folder
"""

import os

from app.experiment.models import Experiment
from config import Config
from flask import current_app as app


class ExperimentList(object):
    """
    Handle the information of the experiments of the directory
    """
    exps = []

    def __init__(self, directory=None):
        """
        Initialisation of the experiment list

        Args:
          directory: str
            The working directory path
        """
        self.load(directory=directory)

    def load(self, directory=None):
        """
        Load the information of the experiment list from the working directory

        Args:
          directory: str
            The working directory path
        """
        self.exps = []
        if directory is None:
            directory = Config.WORKING_DIR
        for exp_dir in os.listdir(directory):
            try:
                self.exps.append(
                        Experiment(directory=os.path.join(directory, exp_dir))
                        )
            # In case of empty dir or dir without info.json file
            except FileNotFoundError:
                continue
            except Exception as e:
                app.logger.error('Unknown error occured while loading json files from experiment folder: %s' %e,)

    def to_dict(self):
        """
        Convert to dict for serialisation

        Returns
          dict: the result dictionnary
        """

        return({exp.expid: exp.to_dict() for exp in self.exps})
