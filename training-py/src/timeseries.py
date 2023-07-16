import os
import uuid
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import statsmodels.api as sm
import seaborn as sb
from statsmodels.tsa.stattools import acf, pacf
from src import logger
sb.set_style('darkgrid')

def get_ts_data(sravzid, price_df, col):
    vertical_sections = 18
    widthInch = 10
    heightInch = vertical_sections * 5
    fig = plt.figure(figsize=(widthInch, heightInch))
    gs = gridspec.GridSpec(vertical_sections, 4, wspace=1, hspace=0.5)
    gs.update(left=0.1, right=0.9, top=0.965, bottom=0.03)

    ax_price_df = plt.subplot(gs[0, :])
    price_df.plot(ax=ax_price_df)
    ax_price_df.set_title("{0} {1} Price Vs Date".format(sravzid, col))

    ax_first_difference = plt.subplot(gs[1, :])
    price_df['First Difference'] = price_df[col] - price_df[col].shift()
    price_df['First Difference'].plot(ax=ax_first_difference)
    ax_first_difference.set_title(
        "{0} {1} Price First Difference Vs Date".format(sravzid, col))

    ax_natural_log = plt.subplot(gs[2, :])
    price_df['Natural Log'] = price_df[col].apply(lambda x: np.log(x))
    price_df['Natural Log'].plot(ax=ax_natural_log)
    ax_natural_log.set_title(
        "{0} {1} Price Natual Log Vs Date".format(sravzid, col))

    ax_original_variance = plt.subplot(gs[3, :2])
    ax_natual_log_variance = plt.subplot(gs[3, 2:])
    price_df['Original Variance'] = price_df[col].rolling(30, min_periods=None, center=True).var()
    price_df['Log Variance'] = price_df['Natural Log'].rolling(30, min_periods=None, center=True).var()
    price_df['Original Variance'].plot(ax=ax_original_variance,
                                        title="{0} {1} Price Original Variance Vs Date".format(sravzid, col))
    price_df['Log Variance'].plot(ax=ax_natual_log_variance,
                                    title="{0} {1} Price Log Variance Vs Date".format(sravzid, col))

    ax_logged_first_difference = plt.subplot(gs[4, :])
    price_df['Logged First Difference'] = price_df['Natural Log'] - \
        price_df['Natural Log'].shift()
    price_df['Logged First Difference'].plot(ax=ax_logged_first_difference,
                                                title="{0} {1} Price Logged First Difference Vs Date".format(sravzid, col))

    ax_lag_correlation = plt.subplot(gs[5, :])
    lag_correlations = acf(price_df['Logged First Difference'].iloc[1:])
    ax_lag_correlation.plot(lag_correlations, marker='o', linestyle='--')
    ax_lag_correlation.set_title(
        "Complete Historical Data: {0} {1} Price Logged First Difference Auto correlation Vs Lag Step".format(sravzid, col))

    ax_lag_partial_auto_correlation = plt.subplot(gs[6, :])
    lag_partial_correlations = pacf(
        price_df['Logged First Difference'].iloc[1:])
    ax_lag_partial_auto_correlation.plot(
        lag_partial_correlations, marker='o', linestyle='--')
    ax_lag_partial_auto_correlation.set_title(
        "Complete Historical Data: {0} {1} Price Logged First Difference Partial Auto correlation Vs Lag Step".format(sravzid, col))

    ax_lag_correlation_10yrs = plt.subplot(gs[7, :])
    lag_correlations = acf(price_df['Logged First Difference'].last('10Y').iloc[1:])
    ax_lag_correlation_10yrs.plot(lag_correlations, marker='o', linestyle='--')
    ax_lag_correlation_10yrs.set_title(
        "Last 10 yrs: {0} {1} Price Logged First Difference Auto correlation Vs Lag Step".format(sravzid, col))

    ax_lag_partial_auto_correlation_10yrs = plt.subplot(gs[8, :])
    lag_partial_correlations = pacf(
        price_df['Logged First Difference'].last('10Y').iloc[1:])
    ax_lag_partial_auto_correlation_10yrs.plot(
        lag_partial_correlations, marker='o', linestyle='--')
    ax_lag_partial_auto_correlation_10yrs.set_title(
        "Last 10 yrs: {0} {1} Price Logged First Difference Partial Auto correlation Vs Lag Step".format(sravzid, col))
    
    ax_lag_correlation_5yrs = plt.subplot(gs[9, :])
    lag_correlations = acf(price_df['Logged First Difference'].last('5Y').iloc[1:])
    ax_lag_correlation_5yrs.plot(lag_correlations, marker='o', linestyle='--')
    ax_lag_correlation_5yrs.set_title(
        "Last 5 yrs: {0} {1} Price Logged First Difference Auto correlation Vs Lag Step".format(sravzid, col))

    ax_lag_partial_auto_correlation_5yrs = plt.subplot(gs[10, :])
    lag_partial_correlations = pacf(
        price_df['Logged First Difference'].last('5Y').iloc[1:])
    ax_lag_partial_auto_correlation_5yrs.plot(
        lag_partial_correlations, marker='o', linestyle='--')
    ax_lag_partial_auto_correlation_5yrs.set_title(
        "Last 5 yrs: {0} {1} Price Logged First Difference Partial Auto correlation Vs Lag Step".format(sravzid, col))

    ax_lag_correlation_2yrs = plt.subplot(gs[11, :])
    lag_correlations = acf(price_df['Logged First Difference'].last('2Y').iloc[1:])
    ax_lag_correlation_2yrs.plot(lag_correlations, marker='o', linestyle='--')
    ax_lag_correlation_2yrs.set_title(
        "Last 2 yrs: {0} {1} Price Logged First Difference Auto correlation Vs Lag Step".format(sravzid, col))

    ax_lag_partial_auto_correlation_2yrs = plt.subplot(gs[12, :])
    lag_partial_correlations = pacf(
        price_df['Logged First Difference'].last('2Y').iloc[1:])
    ax_lag_partial_auto_correlation_2yrs.plot(
        lag_partial_correlations, marker='o', linestyle='--')
    ax_lag_partial_auto_correlation_2yrs.set_title(
        "Last 2 yrs: {0} {1} Price Logged First Difference Partial Auto correlation Vs Lag Step".format(sravzid, col))     

    ax_lag_correlation_1yrs = plt.subplot(gs[13, :])
    lag_correlations = acf(price_df['Logged First Difference'].last('1Y').iloc[1:])
    ax_lag_correlation_1yrs.plot(lag_correlations, marker='o', linestyle='--')
    ax_lag_correlation_1yrs.set_title(
        "Last 1 yrs: {0} {1} Price Logged First Difference Auto correlation Vs Lag Step".format(sravzid, col))

    ax_lag_partial_auto_correlation_1yrs = plt.subplot(gs[14, :])
    lag_partial_correlations = pacf(
        price_df['Logged First Difference'].last('1Y').iloc[1:])
    ax_lag_partial_auto_correlation_1yrs.plot(
        lag_partial_correlations, marker='o', linestyle='--')
    ax_lag_partial_auto_correlation_1yrs.set_title(
        "Last 1 yrs: {0} {1} Price Logged First Difference Partial Auto correlation Vs Lag Step".format(sravzid, col))            

    try:
        ax_natual_log_vs_forecast = plt.subplot(gs[15, :])
        model = sm.tsa.ARIMA(price_df['Natural Log'].iloc[1:], order=(1, 0, 0))
        results = model.fit(disp=-1)
        price_df['Forecast'] = results.fittedvalues
        price_df[['Natural Log', 'Forecast']].plot(ax=ax_natual_log_vs_forecast,
                                                title="{0} {1} Price Logged & Forecast Vs Date".format(sravzid, col))
    except Exception:
        logger.logging.exception('ARIMR error')

    try:
        ax_logged_first_difference_vs_forecast = plt.subplot(gs[16, :])
        model = sm.tsa.ARIMA(
            price_df['Logged First Difference'].iloc[1:], order=(1, 0, 0))
        results = model.fit(disp=-1)
        price_df['Forecast'] = results.fittedvalues
        price_df[['Logged First Difference', 'Forecast']].plot(ax=ax_logged_first_difference_vs_forecast,
                                                            title="{0} {1} Price Logged First Difference & Forecast Vs Date".format(sravzid, col))
    except Exception:
        logger.logging.exception('Logged first difference vs Forecast error')

    try:
        ax_expoential_smooth_logged_first_difference_vs_forecast = plt.subplot(
            gs[17, :])
        model = sm.tsa.ARIMA(
            price_df['Logged First Difference'].iloc[1:], order=(0, 0, 1))
        results = model.fit(disp=-1)
        price_df['Exponential Smoothing Forecast'] = results.fittedvalues
        price_df[['Logged First Difference',
                'Exponential Smoothing Forecast']].plot(ax=ax_expoential_smooth_logged_first_difference_vs_forecast,
                                                        title="{0} {1} Price Logged First Difference & Exponential Smooth Forecast Vs Date".format(sravzid, col))
    except Exception:
        logger.logging.exception('Logged first difference vs Exponential Smoothing Forecast error')
