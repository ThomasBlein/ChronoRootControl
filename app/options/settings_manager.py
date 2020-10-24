"""
Handle the information of one experiment
"""

from config import Config


class Settings(object):
    """
    Handle the information of one experiment
    """
    def __init__(self):
        """Set Settings object from Config file
        """
        for attr, value in Config.__dict__.items():
            if not attr.startswith('__'):
                self.__setattr__(attr, value)
            

            