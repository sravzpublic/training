import datetime
import traceback
import uuid
from functools import reduce
from . import util
from bson.objectid import ObjectId
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from src import logger

class engine(object):
    """Asset engine"""

    def __init__(self):
        self.logger = logger.RotatingLogger(__name__).getLogger()

    def get_historical_price(self, sravzid):
        '''
            ae = engine()
            ae.get_historical_price('fut_gold')
        '''
        return pd.read_csv('{0}{1}.csv'.format(util.constants.DATA_FILE_LOCATION, sravzid), index_col=0)

    def get_assets(self, sravzids):
        data_dfs = []
        for sravzid in sravzids:
            price_df = self.get_historical_price(sravzid)
            column_names = {}
            [column_names.update({name: "%s%s" % (name, sravzid)})
            for name in price_df.columns if name != 'Date']
            price_df = price_df.rename(index=str, columns=column_names)
            data_dfs.append(price_df)
            # Outer join all data frame on Data column
            data_df = reduce(lambda  left,right: pd.merge(left,right,on=['Date'],
                    how='outer'), data_dfs).fillna(method='bfill')
            #sort price in the decending order of date
            data_df = data_df.sort_values(by='Date', ascending=False)
            data_df.index = pd.to_datetime(data_df.index)
            return data_df

    def get_combined_charts(self, sravzids):
        data_df = self.get_assets(sravzids)

        vertical_sections = len(util.constants.ChartsToDisplayAndAcceptedColumns)
        widthInch = 10
        heightInch = vertical_sections * 3
        fig = plt.figure(figsize=(widthInch, heightInch))

        gs = gridspec.GridSpec(vertical_sections, 4, wspace=1, hspace=0.5)
        gs.update(left=0.1, right=0.9, top=0.965, bottom=0.03)

        i = 0
        for key, value in util.constants.ChartsToDisplayAndAcceptedColumns.items():
            # Plot Settle for Futures and Last for Stocks on the same plot
            df_to_plot = data_df[[x for x in data_df.columns if any([y for y in value if y in x.lower()])]]
            if not df_to_plot.empty:
                try:
                    ax_plot = plt.subplot(gs[i, :])
                    df_to_plot.plot(kind='line', ax=ax_plot)
                    i = i+1
                except Exception:
                    self.logger.exception('Error plotting data for columns {0}'.format([
                        x for x in df_to_plot.columns if key in x.lower()]))

        fig.show()