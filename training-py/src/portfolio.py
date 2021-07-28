#!/usr/bin/env python
# Reference: https://jakevdp.github.io/PythonDataScienceHandbook/05.09-principal-component-analysis.html
import datetime
import traceback
import uuid
from functools import reduce
from src import asset, logger, util
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import seaborn as sns
from sklearn.decomposition import PCA
from scipy import stats

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
                price_df = self.ae.get_historical_price(sravzid)[['AdjustedClose']]
                price_df = price_df.sort_index(ascending=False)
                #bfill price data: price is in descending order of date
                price_df['AdjustedClose'] = price_df['AdjustedClose'].pct_change(periods=1)
                #rename columns: cannot have multiple Last column in the same data frame
                price_df = price_df.rename(columns={'AdjustedClose': '%s_adjustedclose_pct_chg' % (sravzid)})
                # Append all the price dataframe to an array
                data_dfs.append(price_df)
            except Exception:
                self.logger.error('Failed to process sravz_id %s' %
                                  (sravzid), exc_info=True)
        if data_dfs and len(data_dfs) > 1:
            # Outer join all data frame on Date column
            data_df = reduce(lambda  left,right: pd.merge(left,right, left_index = True, right_index=True,
                             how='outer'), data_dfs)
            #sort price in the decending order of date
            data_df = data_df.sort_index(ascending=False)
        else:
            data_df = data_dfs.pop()
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

    def get_portfolio_daily_returns(self, portfolio_assets_returns_df):
        '''
            returns portfolio daily returns df
        '''
        numstocks = len(portfolio_assets_returns_df.columns)
        portfolio_weights_ew = np.repeat(1/numstocks, numstocks)
        return portfolio_assets_returns_df.iloc[:, 0:numstocks].mul(portfolio_weights_ew, axis=1).sum(axis=1)

    def get_portfolio_cummulative_returns(self, name, user_id, portfolio_assets=None):
        '''
            returns portfolio daily returns df
        '''
        return ((1+self.get_portfolio_daily_returns(name, user_id, portfolio_assets=portfolio_assets)).cumprod()-1)

    def create_portfolio_correlation_report(self, portofolio_assets_daily_returns,
                                            portofolio_daily_returns,
                                            return_fig = False):
        vertical_sections = 5
        no_of_assets = len(portofolio_assets_daily_returns.columns)
        widthInch = 10 + no_of_assets * 3
        heightInch = vertical_sections * 5 + no_of_assets * 3
        fig = plt.figure(figsize=(widthInch, heightInch))

        gs = gridspec.GridSpec(vertical_sections, 4, wspace=1, hspace=0.5)
        gs.update(left=0.1, right=0.9, top=0.965, bottom=0.03)

        i = 0
        ax_cov_matrix = plt.subplot(gs[i, 1:])
        cov_matrix = portofolio_assets_daily_returns.cov().round(5)
        #ax2 = fig.add_subplot(122)
        font_size = 14
        bbox = [0, 0, 1, 1]
        ax_cov_matrix.axis('off')
        mpl_table = ax_cov_matrix.table(
            cellText=cov_matrix.values, rowLabels=cov_matrix.index, bbox=bbox, colLabels=cov_matrix.columns)
        mpl_table.auto_set_font_size(False)
        mpl_table.set_fontsize(font_size)
        ax_cov_matrix.set_title("Covariance matrix last % daily returns")

        i = 1
        ax_corr_matrix = plt.subplot(gs[i, 1:])
        corr_matrix = portofolio_assets_daily_returns.corr().round(5)
        #ax2 = fig.add_subplot(122)
        font_size = 14
        bbox = [0, 0, 1, 1]
        ax_corr_matrix.axis('off')
        mpl_table = ax_corr_matrix.table(
            cellText=corr_matrix.values, rowLabels=corr_matrix.index, bbox=bbox, colLabels=corr_matrix.columns)
        #mpl_table.set_xticklabels(corr_matrix.index, rotation=45)
        mpl_table.auto_set_font_size(False)
        mpl_table.set_fontsize(font_size)
        ax_corr_matrix.set_title("Correlation matrix last % daily returns")

        i = 2
        ax_corr_heat_map = plt.subplot(gs[i:4, :])
        ax_corr_heat_map.set_title("Correlation matrix heatmap last % daily returns")
        ax = sns.heatmap(
            corr_matrix,
            ax = ax_corr_heat_map,
            vmin=-1, vmax=1, center=0,
            cmap=sns.diverging_palette(20, 220, n=200),
            square=True
        )
        ax.set_xticklabels(
            ax.get_xticklabels(),
            rotation=45,
            horizontalalignment='right'
        )

    def get_scatter_plot_daily_return(self, sravzids):
        '''
        '''
        vertical_sections = 3
        widthInch = 10 + len(sravzids) * 3
        heightInch = vertical_sections * 10 + len(sravzids) * 5
        fig = plt.figure(figsize=(widthInch, heightInch))

        gs = gridspec.GridSpec(vertical_sections, 3, wspace=1, hspace=0.5)
        gs.update(left=0.1, right=0.9, top=0.965, bottom=0.03)

        i = 0

        scatter_plot_df = self.get_percent_daily_returns(sravzids)
        _data = scatter_plot_df.replace([np.inf, -np.inf], np.nan).fillna(0)
        # Set number of components to 2
        n_components = 2
        # Create Principal Components Analysis object with number of expected components
        _p = PCA(n_components=n_components)
        # Fit the daily returns data to the N components
        pca_dat = _p.fit(_data)
        fig = plt.figure()

        ax_first_pc_variance_explanation = plt.subplot(gs[i, :])
        # Display variance explained by each Principal Component
        ax_first_pc_variance_explanation.bar(range(n_components), pca_dat.explained_variance_ratio_)
        ax_first_pc_variance_explanation.set_title('Variance explained by first {0} principal components'.format(n_components))

        #plt.bar(range(n_components), pca_dat.explained_variance_ratio_)
        #plt.title('Variance explained by first {0} principal components'.format(n_components))

        i = 1
        pc_vs_index_returns_pc1 = plt.subplot(gs[i, :])        
        first_pc = pca_dat.components_[0]
        first_pc_normalized_to_1 = np.asmatrix(first_pc/sum(first_pc)).T
        first_pc_portfolio_return = scatter_plot_df.values*first_pc_normalized_to_1
        pc_ret = pd.DataFrame(data=first_pc_portfolio_return, index=scatter_plot_df.index)
        # Reconstruct the actual price from the percent daily returns
        pc_ret_idx = pc_ret+1
        pc_ret_idx = pc_ret_idx.cumprod()
        pc_ret_idx.columns = ['pc1']
        index_column = util.constants.PRICE_COLUMN_TO_USE
        index_retruns_df = self.ae.get_historical_price('idx_us_spx')[
            [index_column]]
        pc_ret_vs_idx_returns = pc_ret_idx.join(index_retruns_df)
        pc_ret_vs_idx_returns['pc1'].plot(
            title='First PC returns', ax=pc_vs_index_returns_pc1)
        i = 2
        pc_vs_index_returns_index = plt.subplot(gs[i, :])            
        pc_ret_vs_idx_returns[index_column].plot(title='Index {0} {1} price returns'.format(
            'idx_us_spx', index_column), ax=pc_vs_index_returns_index)

