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
        data_df = pd.read_csv('{0}{1}.csv'.format(util.constants.DATA_FILE_LOCATION, sravzid), index_col=0)
        data_df.index = pd.to_datetime(data_df.index)
        data_df.index = data_df.index.date
        return data_df

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
                how='outer'), data_dfs).fillna(method='ffill')
        #sort price in the decending order of date
        data_df = data_df.sort_index(ascending=False)
        data_df.index = pd.to_datetime(data_df.index)
        data_df.index = data_df.index.date
        return data_df

    def get_combined_charts(self, sravzids):
        data_df = self.get_assets(sravzids)

        # Display chart, head and tail
        vertical_sections = len(util.constants.ChartsToDisplayAndAcceptedColumns) * 3
        widthInch = 10
        heightInch = vertical_sections * 3
        fig = plt.figure(figsize=(widthInch, heightInch))

        gs = gridspec.GridSpec(vertical_sections, 4, wspace=1, hspace=0.5)
        gs.update(left=0.1, right=0.9, top=0.965, bottom=0.03)

        i = 0
        fig.suptitle("Combined chart as of {0}".format(datetime.datetime.utcnow()))
        for key, value in util.constants.ChartsToDisplayAndAcceptedColumns.items():
            # Plot Settle for Futures and Last for Stocks on the same plot
            df_to_plot = data_df[[x for x in data_df.columns if any([y for y in value if y in x.lower()])]]
            if not df_to_plot.empty:
                try:
                    ax_plot = plt.subplot(gs[i, :])
                    df_to_plot.plot(kind='line', ax=ax_plot)
                    i = i+1
                    ax_head_df = plt.subplot(gs[i, 1:])
                    df_head = df_to_plot.head()
                    font_size = 14
                    bbox = [0, 0, 1, 1]
                    ax_head_df.axis('off')
                    mpl_table = ax_head_df.table(
                        cellText=df_head.values, rowLabels=df_head.index, bbox=bbox, colLabels=df_head.columns)
                    mpl_table.auto_set_font_size(False)
                    mpl_table.set_fontsize(font_size)
                    ax_head_df.set_title("Latest values")
                    i = i+1
                    ax_tail_df = plt.subplot(gs[i, 1:])
                    df_tail = df_to_plot.tail()
                    font_size = 14
                    bbox = [0, 0, 1, 1]
                    ax_tail_df.axis('off')
                    mpl_table = ax_tail_df.table(
                        cellText=df_tail.values, rowLabels=df_tail.index, bbox=bbox, colLabels=df_tail.columns)
                    mpl_table.auto_set_font_size(False)
                    mpl_table.set_fontsize(font_size)
                    ax_tail_df.set_title("Earliest values")
                    i = i+1
                except Exception:
                    self.logger.exception('Error plotting data for columns {0}'.format([
                        x for x in df_to_plot.columns if key in x.lower()]))

        fig.show()