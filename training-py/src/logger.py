'''
Created on Mar 6, 2017

@author: admin
'''
import logging, sys
from logging.handlers import RotatingFileHandler
from util import constants

class RotatingLogger(object):

    def __init__(self, name, level = None, path = None):
        self.name = name
        self.level = level or logging.INFO
        self.path = path or self.getLogFile()
        self.maxBytes=1024000000
        self.backupCount=5

    def getLogger(self):
        """
        Creates a rotating logger
        """
        logger = logging.getLogger(self.name)
        logger.setLevel(self.level)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        # add a rotating handler
        if not logger.handlers:
            handler = RotatingFileHandler(self.path, self.maxBytes, self.backupCount)
            handler.setFormatter(formatter)
            logger.addHandler(handler)

            # Log to stream for debugging
            streamHandler = logging.StreamHandler(sys.stdout)
            streamHandler.setFormatter(formatter)
            logger.addHandler(streamHandler)

        return logger

    def getLogFile(self):
        return constants.LOG_LOCATION
