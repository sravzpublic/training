#
# Copyright 2016 Quantopian, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from __future__ import division
from statsmodels.tsa.stattools import adfuller
from sklearn.decomposition import PCA
from time import time
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.colors as mcolors
import numpy as np
import scipy.stats
import pandas as pd
import seaborn as sns
from pyfolio import plotting, utils, timeseries
from pyfolio.plotting import plotting_context
from pyfolio import _seaborn as sns
import empyrical
import warnings
import datetime
import os
import matplotlib
import uuid
import empyrical as ep

try:
    from pyfolio import bayesian
    have_bayesian = True
except ImportError:
    warnings.warn("Could not import bayesian submodule due to missing pymc3 dependency.", ImportWarning)
    have_bayesian = False

@plotting_context
def create_returns_tear_sheet(returns, positions=None,
                              live_start_date=None,
                              cone_std=(1.0, 1.5, 2.0),
                              benchmark_rets=None,
                              bootstrap=False,
                              return_fig=False,
                              sravzid = None):
    """
    Generate a number of plots for analyzing a strategy's returns.

    - Fetches benchmarks, then creates the plots on a single figure.
    - Plots: rolling returns (with cone), rolling beta, rolling sharpe,
        rolling Fama-French risk factors, drawdowns, underwater plot, monthly
        and annual return plots, daily similarity plots,
        and return quantile box plot.
    - Will also print the start and end dates of the strategy,
        performance statistics, drawdown periods, and the return range.

    Parameters
    ----------
    returns : pd.Series
        Daily returns of the strategy, noncumulative.
         - See full explanation in create_full_tear_sheet.
    positions : pd.DataFrame, optional
        Daily net position values.
         - See full explanation in create_full_tear_sheet.
    live_start_date : datetime, optional
        The point in time when the strategy began live trading,
        after its backtest period.
    cone_std : float, or tuple, optional
        If float, The standard deviation to use for the cone plots.
        If tuple, Tuple of standard deviation values to use for the cone plots
         - The cone is a normal distribution with this standard deviation
             centered around a linear regression.
    benchmark_rets : pd.Series, optional
        Daily noncumulative returns of the benchmark.
         - This is in the same style as returns.
    bootstrap : boolean (optional)
        Whether to perform bootstrap analysis for the performance
        metrics. Takes a few minutes longer.
    return_fig : boolean, optional
        If True, returns the figure that was plotted on.
    set_context : boolean, optional
        If True, set default plotting style context.
    """

    if benchmark_rets is None:
        benchmark_rets = utils.get_symbol_rets('SPY')
        # If the strategy's history is longer than the benchmark's, limit
        # strategy
        if returns.index[0] < benchmark_rets.index[0]:
            returns = returns[returns.index > benchmark_rets.index[0]]

    print("Entire data start date: %s" % returns.index[0].strftime('%Y-%m-%d'))
    print("Entire data end date: %s" % returns.index[-1].strftime('%Y-%m-%d'))
    print('\n')

    # If the strategy's history is longer than the benchmark's, limit strategy
    if returns.index[0] < benchmark_rets.index[0]:
        returns = returns[returns.index > benchmark_rets.index[0]]

    vertical_sections = 14

    if live_start_date is not None:
        vertical_sections += 1
        live_start_date = utils.get_utc_timestamp(live_start_date)

    if bootstrap:
        vertical_sections += 1

    widthInch = 14
    heightInch = vertical_sections * 5
    fig = plt.figure(figsize=(widthInch, heightInch))

    gs = gridspec.GridSpec(vertical_sections, 3, wspace=1, hspace=0.5)
    gs.update(left=0.1, right=0.9, top=0.965, bottom=0.03)

    perf_stats = plotting.show_perf_stats(returns, benchmark_rets,
                             positions=positions,
                             bootstrap=bootstrap,
                             live_start_date=live_start_date)

    plt.suptitle('%s returns tearsheet as of %s'%(sravzid, datetime.datetime.now().strftime("%m/%d/%Y")))

    i = 0
    ax_perf_stats = plt.subplot(gs[i, 1:])
    font_size = 14
    bbox = [0, 0, 1, 1]
    ax_perf_stats.axis('off')
    mpl_table = ax_perf_stats.table(
        cellText=perf_stats.values, rowLabels=perf_stats.index, bbox=bbox, colLabels=perf_stats.columns)
    mpl_table.auto_set_font_size(False)
    mpl_table.set_fontsize(font_size)
    ax_perf_stats.set_title("Perfomance statistics")


    i += 1
    ax_drawdown_stats = plt.subplot(gs[i, :])
    drawdown_stats = timeseries.gen_drawdown_table(returns, top=5).round(3)
    ax_drawdown_stats.axis('off')
    mpl_table = ax_drawdown_stats.table(
        cellText=drawdown_stats.values, rowLabels=drawdown_stats.index, bbox=bbox, colLabels=drawdown_stats.columns)
    mpl_table.auto_set_font_size(False)
    mpl_table.set_fontsize(font_size)
    ax_drawdown_stats.set_title("Worst Drawdown Statistics")

    # Create axis for plots
    ax_rolling_returns = plt.subplot(gs[2:4, :])
    i += 3
    ax_rolling_returns_vol_match = plt.subplot(gs[i, :],
                                               sharex=ax_rolling_returns)
    i += 1
    ax_rolling_returns_log = plt.subplot(gs[i, :],
                                         sharex=ax_rolling_returns)
    i += 1
    ax_returns = plt.subplot(gs[i, :],
                             sharex=ax_rolling_returns)
    i += 1
    ax_rolling_beta = plt.subplot(gs[i, :], sharex=ax_rolling_returns)
    i += 1
    ax_rolling_sharpe = plt.subplot(gs[i, :], sharex=ax_rolling_returns)
    i += 1
    ax_rolling_risk = plt.subplot(gs[i, :], sharex=ax_rolling_returns)
    i += 1
    ax_drawdown = plt.subplot(gs[i, :], sharex=ax_rolling_returns)
    i += 1
    ax_underwater = plt.subplot(gs[i, :], sharex=ax_rolling_returns)
    i += 1
    ax_monthly_heatmap = plt.subplot(gs[i, 0])
    ax_annual_returns = plt.subplot(gs[i, 1])
    ax_monthly_dist = plt.subplot(gs[i, 2])
    i += 1
    ax_return_quantiles = plt.subplot(gs[i, :])
    i += 1

    # Genereate plots
    plotting.plot_rolling_returns(
        returns,
        factor_returns=benchmark_rets,
        live_start_date=live_start_date,
        cone_std=cone_std,
        ax=ax_rolling_returns)
    ax_rolling_returns.set_title(
        'Cumulative returns')

    plotting.plot_rolling_returns(
        returns,
        factor_returns=benchmark_rets,
        live_start_date=live_start_date,
        cone_std=None,
        volatility_match=True,
        legend_loc=None,
        ax=ax_rolling_returns_vol_match)
    ax_rolling_returns_vol_match.set_title(
        'Cumulative returns volatility matched to benchmark')

    plotting.plot_rolling_returns(
        returns,
        factor_returns=benchmark_rets,
        logy=True,
        live_start_date=live_start_date,
        cone_std=cone_std,
        ax=ax_rolling_returns_log)
    ax_rolling_returns_log.set_title(
        'Cumulative returns on logarithmic scale')

    plotting.plot_returns(
        returns,
        live_start_date=live_start_date,
        ax=ax_returns,
    )
    ax_returns.set_title(
        'Returns')

    plotting.plot_rolling_beta(
        returns, benchmark_rets, ax=ax_rolling_beta)

    plotting.plot_rolling_sharpe(
        returns, ax=ax_rolling_sharpe)

    plotting.plot_rolling_fama_french(
        returns, ax=ax_rolling_risk)

    # Drawdowns
    plotting.plot_drawdown_periods(
        returns, top=5, ax=ax_drawdown)

    plotting.plot_drawdown_underwater(
        returns=returns, ax=ax_underwater)

    plotting.show_worst_drawdown_periods(returns)

    plotting.show_return_range(returns)

    plotting.plot_monthly_returns_heatmap(returns, ax=ax_monthly_heatmap)
    plotting.plot_annual_returns(returns, ax=ax_annual_returns)
    plotting.plot_monthly_returns_dist(returns, ax=ax_monthly_dist)

    plotting.plot_return_quantiles(
        returns,
        live_start_date=live_start_date,
        ax=ax_return_quantiles)

    if bootstrap:
        ax_bootstrap = plt.subplot(gs[i, :])
        plotting.plot_perf_stats(returns, benchmark_rets,
                                 ax=ax_bootstrap)

    for ax in fig.axes:
        plt.setp(ax.get_xticklabels(), visible=True)

    #plt.show()
    #if return_fig:
    #    return fig

def get_rolling_stats(price_df, sravzid, return_fig=True):
    price_df.columns = map(str.lower, price_df.columns)

    col = 'settle'

    vertical_sections = 5
    widthInch = 10
    heightInch = vertical_sections * 5
    fig = plt.figure(figsize=(widthInch, heightInch))
    gs = gridspec.GridSpec(vertical_sections, 4, wspace=1, hspace=0.5)
    gs.update(left=0.1, right=0.9, top=0.965, bottom=0.03)
    chart_index = 0
    ax_price_plot = plt.subplot(gs[chart_index, :])
    price_df[col].plot(label=col, ax=ax_price_plot)
    ax_price_plot.set_title(
        '{0} {1} Price'.format(sravzid, col))
    ax_price_plot.legend()

###
    # ax_price_all_columns_plot = plt.subplot(gs[1, 1:-1])
    # ax_price_all_columns_plot.set_yscale('log')
    # # price_df.plot(ax=ax_price_all_columns_plot)
    # plot_multi(price_df, ax_price_all_columns_plot)
    # ax_price_all_columns_plot.set_title(
    #     '{0} Available Data'.format(sravzid))
    # ax_price_all_columns_plot.legend()
    chart_index = chart_index + 1
    ax_describe = plt.subplot(gs[chart_index, :])
    ax_describe.axis('off')
    describe_df = price_df.describe().round(3)
    font_size = 14
    bbox = [0, 0, 1, 1]
    mpl_table = ax_describe.table(
        cellText=describe_df.values, rowLabels=describe_df.index, bbox=bbox, colLabels=describe_df.columns)
    mpl_table.auto_set_font_size(False)
    mpl_table.set_fontsize(font_size)
    ax_describe.set_title("{0} Summary Statistics".format(sravzid))
###

    chart_index = chart_index + 1
    ax_rolling_mean_plot = plt.subplot(gs[chart_index, :])
    #price_df[col].plot(label=col, ax=ax_rolling_mean_plot)
    price_df[col].rolling(7).mean().plot(
        label="7 days MA", ax=ax_rolling_mean_plot)
    price_df[col].rolling(21).mean().plot(
        label="21 days MA", ax=ax_rolling_mean_plot)
    price_df[col].rolling(255).mean().plot(
        label="255 days MA", ax=ax_rolling_mean_plot)
    ax_rolling_mean_plot.set_title(
        '{0} {1} Rolling Moving Average'.format(sravzid, col))
    ax_rolling_mean_plot.legend()

    chart_index = chart_index + 1
    ax_rolling_std_plot = plt.subplot(gs[chart_index, :])
    #price_df[col].plot(label=col, ax=ax_rolling_std_plot)
    price_df[col].rolling(7).std().plot(
        label="7 days Std", ax=ax_rolling_std_plot)
    price_df[col].rolling(21).std().plot(
        label="21 days Std", ax=ax_rolling_std_plot)
    price_df[col].rolling(255).std().plot(
        label="255 days Std", ax=ax_rolling_std_plot)
    ax_rolling_std_plot.set_title(
        '{0} {1} Rolling Moving Std'.format(sravzid, col))
    ax_rolling_std_plot.legend()

    chart_index = chart_index + 1
    ax_df = plt.subplot(gs[chart_index, 1:])
    series = price_df[col].dropna()
    dftest = adfuller(series, autolag='AIC')
    dfoutput = pd.Series(dftest[0:4], index=[
                         'Test Statistic', 'p-value', '#Lags Used', 'Number of Observations Used'])
    for key, value in list(dftest[4].items()):
        dfoutput['Critical Value (%s)' % key] = value
    font_size = 14
    bbox = [0, 0, 1, 1]
    ax_df.axis('off')
    df_test_df = dfoutput.to_frame()
    mpl_table = ax_df.table(
        cellText=df_test_df.values, rowLabels=df_test_df.index, bbox=bbox, colLabels=df_test_df.index)
    #mpl_table.set_xticklabels(corr_matrix.index, rotation=45)
    mpl_table.auto_set_font_size(False)
    mpl_table.set_fontsize(font_size)
    ax_df.set_title("{0} {1} Price - Dickey Fuller Test".format(sravzid, col))

