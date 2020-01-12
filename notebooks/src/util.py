import pandas as pd
import numpy as np
import io, os
import datetime, locale, uuid, re

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

class Helper(object):
    '''
    Helper methods
    '''

    def __init__(self, params):
        '''

        '''
    @staticmethod
    def get_n_years_back_date(n_years):
        return (datetime.datetime.now() - datetime.timedelta(days=n_years*365)).strftime("%Y-%m-%d")

    @staticmethod
    def get_n_days_back_date(n_days):
        return (datetime.datetime.now() - datetime.timedelta(days=n_days)).strftime("%Y-%m-%d")

    @staticmethod
    def getfloat(value):
        if value and isinstance(value, str):
            value = value.replace(',', '')
            decimal_point_char = locale.localeconv()['decimal_point']
            value = re.sub(r'[^0-9'+decimal_point_char+r']+', '', value)
        try:
            v = float(value)
            return v
        except:
            return 0.0

    @staticmethod
    def getint(value):
        try:
            v = int(value)
            return v
        except:
            return 0

    @staticmethod
    def translate_string_to_number(in_string):
        '''
            #Futures roll, hence get generic ID if future, remove roll date
            from src.util import helper
            helper.util.translate_string_to_number("$10")
        '''
        # Did not work in vagrant
        # return in_string.translate(None, ',$')
        if isinstance(in_string, str):
            return in_string.replace(",", "").replace('$', "")
        return in_string

    @staticmethod
    def get_temp_file():
        return '/tmp/{0}'.format(uuid.uuid4().hex)

    @staticmethod
    def convert_columns_and_index_to_str(df):
        cols_str = [column.decode('utf-8') for column in df.columns if isinstance(column, bytes)]
        if cols_str:
            df.columns = cols_str
        #df.index = [index.decode('utf-8') for index in df.index if isinstance(index, bytes)]
        return df

    @staticmethod
    def test_df(self):
        import sys
        if sys.version_info[0] < 3:
            from StringIO import StringIO
        else:
            from io import StringIO

        import pandas as pd

        TESTDATA = StringIO("""Date,Lastidx_us_spx
        2019-05-28 00:00:00+00:00,2802.39
        2019-05-24 00:00:00+00:00,2826.06
        2019-05-23 00:00:00+00:00,2822.24
        2019-05-22 00:00:00+00:00,2856.27
        2019-05-21 00:00:00+00:00,2864.36
        2019-05-20 00:00:00+00:00,2840.23
        2019-05-17 00:00:00+00:00,2859.53
        2019-05-16 00:00:00+00:00,2876.32
        2019-05-15 00:00:00+00:00,2850.96
        2019-05-14 00:00:00+00:00,2834.41
            """)

        df = pd.read_csv(TESTDATA, sep=",")

        return df
