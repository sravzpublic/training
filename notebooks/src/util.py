import pandas as pd
import numpy as np
import io, os

class constants(object):
    """description of class"""
    LOG_LOCATION = os.environ.get('ENV_LOG_FILE_NAME') or "/tmp/sravz_jobs.log"
    DATA_FILE_LOCATION = "{0}/data/".format(os.getcwd())

    ChartsToDisplayAndAcceptedColumns = {
        # All lower case
        'settle': ['settle', 'last'],
        'change': ['change'],
        'volume': ['volume'],
        'openinterest': ['openinterest']
    }