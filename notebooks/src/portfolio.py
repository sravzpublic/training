#!/usr/bin/env python
import datetime
import traceback
import uuid
from functools import reduce
from src import asset, logger
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class engine(object):
    """Updates portfolio PNL"""

    def __init__(self):
        self.ae = asset.engine()
        self.logger = logger.RotatingLogger(__name__).getLogger()

    def get_percent_daily_returns(self, sravzids):
        '''
            #Returns percent daily returns
            from src import portfolio
            pe = portfolio.engine()
            pe.get_percent_daily_returns(['fut_gold', 'idx_us_spx'])
        '''
        data_dfs = []
        data_df = None
        for sravzid in sravzids:
            try:
                price_df = self.ae.get_historical_price(sravzid)[['Date', 'Last']]
                #bfill price data: price is in descending order of data
                price_df['Last'] = price_df['Last'].pct_change(periods=1, fill_method='bfill')
                #rename columns: cannot have multiple Last column in the same data frame
                price_df = price_df.rename(columns={'Date': 'Date', 'Last': '%s_last_pct_chg' % (sravzid)})
                # Append all the price dataframe to an array
                data_dfs.append(price_df)
            except Exception:
                self.logger.error('Failed to process sravz_id %s' %
                                  (sravzid), exc_info=True)
        if data_dfs:
            # Outer join all data frame on Data column
            data_df = reduce(lambda  left,right: pd.merge(left,right,on=['Date'],
                             how='outer'), data_dfs).fillna(method='bfill')
            #sort price in the decending order of date
            data_df = data_df.sort_values(by='Date', ascending=False)
        return data_df

    def get_portfolio_assets_daily_returns(self, name, user_id, portfolio_assets=None):
        '''
            returns portfolio assets daily returns df
        '''
        if not portfolio_assets:
            returns = self.pcae_engine.get_percent_daily_returns(
                self.util.get_portfolio_assets(name, user_id))
        else:
            returns = self.pcae_engine.get_percent_daily_returns(
                portfolio_assets)
        return returns

    def get_portfolio_assets_cummulative_daily_returns(self, name, user_id, portfolio_assets=None):
        '''
            returns portfolio assets daily returns df
        '''
        return ((1+self.get_portfolio_assets_daily_returns(name, user_id, portfolio_assets=portfolio_assets)).cumprod()-1)

    def get_portfolio_daily_returns(self, name, user_id, portfolio_assets=None):
        '''
            returns portfolio daily returns df
        '''
        if not portfolio_assets:
            returns = self.pcae_engine.get_percent_daily_returns(
                self.util.get_portfolio_assets(name, user_id))
        else:
            returns = self.pcae_engine.get_percent_daily_returns(
                portfolio_assets)
        numstocks = len(returns.columns)
        portfolio_weights_ew = np.repeat(1/numstocks, numstocks)
        return returns.iloc[:, 0:numstocks].mul(portfolio_weights_ew, axis=1).sum(axis=1)

    def get_portfolio_cummulative_returns(self, name, user_id, portfolio_assets=None):
        '''
            returns portfolio daily returns df
        '''
        return ((1+self.get_portfolio_daily_returns(name, user_id, portfolio_assets=portfolio_assets)).cumprod()-1)

