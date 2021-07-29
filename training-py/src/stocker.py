# Source: https://towardsdatascience.com/stock-prediction-in-python-b66555171a2
# Quandl for financial analysis, pandas and numpy for data manipulation
# fbprophet for additive models, #pytrends for Google trend data
import os
import matplotlib
import quandl
import pandas as pd
import numpy as np
import fbprophet
import pytrends
from pytrends.request import TrendReq
# matplotlib pyplot for plotting
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import pandas as pd
from src import logger, util

CHART_TYPE_CREATE_PROPHET_MODEL = 'CHART_TYPE_CREATE_PROPHET_MODEL'
CHART_TYPE_EVALUATE_PREDICTION = 'CHART_TYPE_EVALUATE_PREDICTION'
CHART_TYPE_CHANGE_POINT_PRIOR_ANALYSIS = 'CHART_TYPE_CHANGE_POINT_PRIOR_ANALYSIS'
CHART_TYPE_CHANGE_POINT_PRIOR_VALIDATION = 'CHART_TYPE_CHANGE_POINT_PRIOR_VALIDATION'
CHART_TYPE_EVALUATE_PREDICTION_WITH_CHANGE_POINT = 'CHART_TYPE_EVALUATE_PREDICTION_WITH_CHANGE_POINT'
CHART_TYPE_PREDICT_FUTURE = 'CHART_TYPE_PREDICT_FUTURE'

def create_stocker_tear_sheet(sravz_id, chart_type, returns_df = None, number_of_years_back = 10):
    """
    Generate stocker tear sheet.

    """

    returns_df.index = pd.to_datetime(returns_df.index)

    tickerAnalysis = Stocker(asset_name = sravz_id, returns_df = returns_df, number_of_years_back = number_of_years_back)
    if chart_type == CHART_TYPE_CHANGE_POINT_PRIOR_VALIDATION:
        vertical_sections = 3
    elif chart_type in [CHART_TYPE_EVALUATE_PREDICTION_WITH_CHANGE_POINT, CHART_TYPE_EVALUATE_PREDICTION]:
        vertical_sections = 2
    else:
        vertical_sections = 1
    widthInch = 14
    heightInch = vertical_sections * 8
    fig = plt.figure(figsize=(widthInch, heightInch))

    i = 0
    gs = gridspec.GridSpec(vertical_sections, 3, wspace=1, hspace=0.5)
    gs.update(left=0.1, right=0.9, top=0.965, bottom=0.03)

    ax = plt.subplot(gs[i, :])
    if chart_type == CHART_TYPE_CREATE_PROPHET_MODEL:
        try:
            model, model_data = tickerAnalysis.create_prophet_model(days=90, ax = ax)
        except Exception:
            logger.logging.exception("Error plotting create_prophet_model")

    if chart_type == CHART_TYPE_EVALUATE_PREDICTION:
        details = tickerAnalysis.evaluate_prediction(ax = ax)
        i = 1
        evaluate_prediction_details_df = pd.DataFrame.from_dict(details, orient='index')
        ax_evaluate_prediction_details_df = plt.subplot(gs[i, 1:])
        font_size = 14
        bbox = [0, 0, 1, 1]
        ax_evaluate_prediction_details_df.axis('off')
        mpl_table = ax_evaluate_prediction_details_df.table(
            cellText=evaluate_prediction_details_df.values, rowLabels=evaluate_prediction_details_df.index, bbox=bbox, colLabels=evaluate_prediction_details_df.columns)
        mpl_table.auto_set_font_size(False)
        mpl_table.set_fontsize(font_size)
        ax_evaluate_prediction_details_df.set_title("Prediction Evaluation")

    if chart_type == CHART_TYPE_CHANGE_POINT_PRIOR_ANALYSIS:
        try:
            tickerAnalysis.changepoint_prior_analysis(changepoint_priors=[0.001, 0.05, 0.1, 0.2], ax = ax)
        except Exception:
            logger.logging.exception("Error plotting changepoint_prior_analysis")

    # # i += 1
    # # ax_changepoint_prior_validation_1 = plt.subplot(gs[i, :])
    # # i += 1
    # # ax_changepoint_prior_validation_2 = plt.subplot(gs[i, :])
    # # tickerAnalysis.changepoint_prior_validation(changepoint_priors=[0.001, 0.05, 0.1, 0.2], ax1=ax_changepoint_prior_validation_1, ax2=ax_changepoint_prior_validation_2)

    if chart_type == CHART_TYPE_CHANGE_POINT_PRIOR_VALIDATION:
        i += 1
        ax2 = plt.subplot(gs[i, :])
        i += 1
        ax3 = plt.subplot(gs[i, :])
        try:
            tickerAnalysis.changepoint_prior_validation(changepoint_priors=[0.001, 0.05, 0.1, 0.2], ax1=ax, ax2=ax2, ax3=ax3)
        except Exception:
            logger.logging.exception("Error plotting changepoint_prior_validation")


    if chart_type == CHART_TYPE_EVALUATE_PREDICTION_WITH_CHANGE_POINT:
        tickerAnalysis.changepoint_prior_scale = 0.5
        try:
            details = tickerAnalysis.evaluate_prediction(ax = ax)
            i = 1
            evaluate_prediction_details_df = pd.DataFrame.from_dict(details, orient='index')
            ax_evaluate_prediction_details_df = plt.subplot(gs[i, 1:])
            font_size = 14
            bbox = [0, 0, 1, 1]
            ax_evaluate_prediction_details_df.axis('off')
            mpl_table = ax_evaluate_prediction_details_df.table(
                cellText=evaluate_prediction_details_df.values, rowLabels=evaluate_prediction_details_df.index, bbox=bbox, colLabels=evaluate_prediction_details_df.columns)
            mpl_table.auto_set_font_size(False)
            mpl_table.set_fontsize(font_size)
            ax_evaluate_prediction_details_df.set_title("Prediction Evaluation")
        except Exception:
            logger.logging.exception("Error plotting evaluate_prediction")

    if chart_type == CHART_TYPE_PREDICT_FUTURE:
        try:
            tickerAnalysis.predict_future(ax = ax)
        except Exception:
            logger.logging.exception("Error plotting predict_future")

    # return fig

# Class for analyzing and (attempting) to predict future prices
# Contains a number of visualizations and analysis methods
class Stocker():

    # Initialization requires a ticker symbol
    def __init__(self, asset_name = None, returns_df = None, number_of_years_back = 10, exchange='WIKI'):

        self.symbol = asset_name
        stock = returns_df
        stock['y'] = stock['AdjustedClose']

        stock = stock[stock.index > util.Helper.get_n_years_back_date(number_of_years_back)]
        # Columns required for prophet
        stock['ds'] = stock.index.values
        stock['Date'] = stock.index.values

        # Data assigned as class attribute
        self.stock = stock.copy()

        # Minimum and maximum date in range
        self.min_date = min(stock['Date'])
        self.max_date = max(stock['Date'])

        # Find max and min prices and dates on which they occurred
        self.max_price = np.max(self.stock['y'])
        self.min_price = np.min(self.stock['y'])

        self.min_price_date = self.stock[self.stock['y'] == self.min_price]['Date']
        self.min_price_date = self.min_price_date[self.min_price_date.index[0]]
        self.max_price_date = self.stock[self.stock['y'] == self.max_price]['Date']
        self.max_price_date = self.max_price_date[self.max_price_date.index[0]]


        # Whether or not to round dates
        self.round_dates = True

        # Number of years of data to train on
        self.training_years = 3

        # Prophet parameters
        # Default prior from library
        self.changepoint_prior_scale = 0.05
        self.weekly_seasonality = False
        self.daily_seasonality = False
        self.monthly_seasonality = True
        self.yearly_seasonality = True
        self.changepoints = None

        print('{} Stocker Initialized. Data covers {} to {}.'.format(self.symbol,
                                                                     self.min_date,
                                                                     self.max_date))

    """
    Make sure start and end dates are in the range and can be
    converted to pandas datetimes. Returns dates in the correct format
    """
    def handle_dates(self, start_date, end_date):


        # Default start and end date are the beginning and end of data
        if start_date is None:
            start_date = self.min_date
        if end_date is None:
            end_date = self.max_date

        try:
            # Convert to pandas datetime for indexing dataframe
            start_date = pd.to_datetime(start_date)
            end_date = pd.to_datetime(end_date)

        except Exception as e:
            print('Enter valid pandas date format.')
            print(e)
            return

        valid_start = False
        valid_end = False

        # User will continue to enter dates until valid dates are met
        while (not valid_start) & (not valid_end):
            valid_end = True
            valid_start = True

            if end_date < start_date:
                print('End Date must be later than start date.')
                start_date = pd.to_datetime(input('Enter a new start date: '))
                end_date= pd.to_datetime(input('Enter a new end date: '))
                valid_end = False
                valid_start = False

            else:
                if end_date > self.max_date:
                    print('End Date exceeds data range')
                    end_date= pd.to_datetime(input('Enter a new end date: '))
                    valid_end = False

                if start_date < self.min_date:
                    print('Start Date is before date range')
                    start_date = pd.to_datetime(input('Enter a new start date: '))
                    valid_start = False


        return start_date, end_date

    """
    Return the dataframe trimmed to the specified range.
    """
    def make_df(self, start_date, end_date, df=None):

        # Default is to use the object stock data
        if not df:
            df = self.stock.copy()


        start_date, end_date = self.handle_dates(start_date, end_date)

        # keep track of whether the start and end dates are in the data
        start_in = True
        end_in = True

        # If user wants to round dates (default behavior)
        if self.round_dates:
            # Record if start and end date are in df
            if (start_date not in list(df['Date'])):
                start_in = False
            if (end_date not in list(df['Date'])):
                end_in = False

            # If both are not in dataframe, round both
            if (not end_in) & (not start_in):
                trim_df = df[(df['Date'] >= start_date) &
                             (df['Date'] <= end_date)]

            else:
                # If both are in dataframe, round neither
                if (end_in) & (start_in):
                    trim_df = df[(df['Date'] >= start_date) &
                                 (df['Date'] <= end_date)]
                else:
                    # If only start is missing, round start
                    if (not start_in):
                        trim_df = df[(df['Date'] > start_date) &
                                     (df['Date'] <= end_date)]
                    # If only end is imssing round end
                    elif (not end_in):
                        trim_df = df[(df['Date'] >= start_date) &
                                     (df['Date'] < end_date)]


        else:
            valid_start = False
            valid_end = False
            while (not valid_start) & (not valid_end):
                start_date, end_date = self.handle_dates(start_date, end_date)

                # No round dates, if either data not in, print message and return
                if (start_date in list(df['Date'])):
                    valid_start = True
                if (end_date in list(df['Date'])):
                    valid_end = True

                # Check to make sure dates are in the data
                if (start_date not in list(df['Date'])):
                    print('Start Date not in data (either out of range or not a trading day.)')
                    start_date = pd.to_datetime(input(prompt='Enter a new start date: '))

                elif (end_date not in list(df['Date'])):
                    print('End Date not in data (either out of range or not a trading day.)')
                    end_date = pd.to_datetime(input(prompt='Enter a new end date: ') )

            # Dates are not rounded
            trim_df = df[(df['Date'] >= start_date) &
                         (df['Date'] <= end_date.date)]



        return trim_df


    # Method to linearly interpolate prices on the weekends
    def resample(self, dataframe):
        # Change the index and resample at daily level
        dataframe = dataframe.set_index('ds')
        dataframe = dataframe.resample('D')

        # Reset the index and interpolate nan values
        dataframe = dataframe.reset_index(level=0)
        dataframe = dataframe.interpolate()
        return dataframe

    # Remove weekends from a dataframe
    def remove_weekends(self, dataframe):

        # Reset index to use ix
        dataframe = dataframe.reset_index(drop=True)

        weekends = []

        # Find all of the weekends
        for i, date in enumerate(dataframe['ds']):
            if (date.weekday()) == 5 | (date.weekday() == 6):
                weekends.append(i)

        # Drop the weekends
        dataframe = dataframe.drop(weekends, axis=0)

        return dataframe


    # Calculate and plot profit from buying and holding shares for specified date range
    def buy_and_hold(self, start_date=None, end_date=None, nshares=1):
        # self.reset_plot()

        start_date, end_date = self.handle_dates(start_date, end_date)

        # Find starting and ending price of stock
        start_price = float(self.stock[self.stock['Date'] == start_date]['Adj. Open'])
        end_price = float(self.stock[self.stock['Date'] == end_date]['Adj. Close'])

        # Make a profit dataframe and calculate profit column
        profits = self.make_df(start_date, end_date)
        profits['hold_profit'] = nshares * (profits['Adj. Close'] - start_price)

        # Total profit
        total_hold_profit = nshares * (end_price - start_price)

        print('{} Total buy and hold profit from {} to {} for {} shares = ${:.2f}'.format
              (self.symbol, start_date, end_date, nshares, total_hold_profit))

        # Location for number of profit
        text_location = (end_date - pd.DateOffset(months = 1))

        # Plot the profits over time
        plt.plot(profits['Date'], profits['hold_profit'], 'b', linewidth = 3)
        plt.ylabel('Profit ($)'); plt.xlabel('Date'); plt.title('Buy and Hold Profits for {} {} to {}'.format(
                                                                self.symbol, start_date, end_date))

        # Display final value on graph
        plt.text(x = text_location,
             y =  total_hold_profit + (total_hold_profit / 40),
             s = '$%d' % total_hold_profit,
            color = 'g' if total_hold_profit > 0 else 'r',
            size = 14)

        plt.grid(alpha=0.2)
        plt.show()

    # Create a prophet model without training
    def create_model(self):

        # Make the model
        model = fbprophet.Prophet(daily_seasonality=self.daily_seasonality,
                                  weekly_seasonality=self.weekly_seasonality,
                                  yearly_seasonality=self.yearly_seasonality,
                                  changepoint_prior_scale=self.changepoint_prior_scale,
                                  changepoints=self.changepoints)

        if self.monthly_seasonality:
            # Add monthly seasonality
            model.add_seasonality(name = 'monthly', period = 30.5, fourier_order = 5)

        return model

    # Graph the effects of altering the changepoint prior scale (cps)
    def changepoint_prior_analysis(self, changepoint_priors=[0.001, 0.05, 0.1, 0.2], colors=['b', 'r', 'grey', 'gold'], ax = None):

        # Training and plotting with specified years of data
        train = self.stock[(self.stock['Date'] > (max(self.stock['Date']) - pd.DateOffset(years=self.training_years)))]

        # Iterate through all the changepoints and make models
        for i, prior in enumerate(changepoint_priors):
            # Select the changepoint
            self.changepoint_prior_scale = prior

            # Create and train a model with the specified cps
            model = self.create_model()
            model.fit(train)
            future = model.make_future_dataframe(periods=180, freq='D')

            # Make a dataframe to hold predictions
            if i == 0:
                predictions = future.copy()

            future = model.predict(future)

            # Fill in prediction dataframe
            predictions['%.3f_yhat_upper' % prior] = future['yhat_upper']
            predictions['%.3f_yhat_lower' % prior] = future['yhat_lower']
            predictions['%.3f_yhat' % prior] = future['yhat']

        # Remove the weekends
        predictions = self.remove_weekends(predictions)

        # Actual observations
        ax.plot(train['ds'], train['y'], 'ko', ms = 4, label = 'Observations')
        color_dict = {prior: color for prior, color in zip(changepoint_priors, colors)}

        # Plot each of the changepoint predictions
        for prior in changepoint_priors:
            # Plot the predictions themselves
            ax.plot(predictions['ds'], predictions['%.3f_yhat' % prior], linewidth = 1.2,
                     color = color_dict[prior], label = '%.3f prior scale' % prior)

            # Plot the uncertainty interval
            ax.fill_between(predictions['ds'].dt.to_pydatetime(), predictions['%.3f_yhat_upper' % prior],
                            predictions['%.3f_yhat_lower' % prior], facecolor = color_dict[prior],
                            alpha = 0.3, edgecolor = 'k', linewidth = 0.6)

        # Plot labels
        ax.legend(loc = 2, prop={'size': 10})
        plt.xlabel('Date')
        plt.ylabel('Stock Price ($)'); plt.title('Effect of Changepoint Prior Scale')
        # plt.show()

        # file_path = helper.util.get_temp_file()
        # fig.savefig(file_path)
        # plt.close(fig)

        # return file_path

    # Basic prophet model for specified number of days
    def create_prophet_model(self, days=0, resample=False, ax = None):

        # self.reset_plot()

        model = self.create_model()

        # Fit on the stock history for self.training_years number of years
        stock_history = self.stock[self.stock['Date'] > (self.max_date - pd.DateOffset(years = self.training_years))]

        if resample:
            stock_history = self.resample(stock_history)

        model.fit(stock_history)

        # Make and predict for next year with future dataframe
        future = model.make_future_dataframe(periods = days, freq='D')
        future = model.predict(future)

        if days > 0:
            # Print the predicted price
            print('Predicted Price on {} = ${:.2f}'.format(
                future.loc[future.index[-1], 'ds'], future.loc[future.index[-1], 'yhat']))

            title = '%s Historical and Predicted Stock Price'  % self.symbol
        else:
            title = '%s Historical and Modeled Stock Price' % self.symbol

        # Set up the plot
        # fig, ax = plt.subplots(1, 1)

        # Plot the actual values
        ax.plot(stock_history['ds'], stock_history['y'], 'ko-', linewidth = 1.4, alpha = 0.8, ms = 1.8, label = 'Observations')

        # Plot the predicted values
        ax.plot(future['ds'], future['yhat'], 'forestgreen',linewidth = 2.4, label = 'Modeled')

        # Plot the uncertainty interval as ribbon
        ax.fill_between(future['ds'].dt.to_pydatetime(), future['yhat_upper'], future['yhat_lower'], alpha = 0.3,
                       facecolor = 'g', edgecolor = 'k', linewidth = 1.4, label = 'Confidence Interval')

        # Plot formatting
        ax.legend(loc = 2, prop={'size': 10}); plt.xlabel('Date'); plt.ylabel('Price $')
        ax.grid(linewidth=0.6, alpha = 0.6)
        ax.set_title(title)
        # plt.title(title)
        # plt.show()

        #file_path = helper.util.get_temp_file()
        #fig.savefig(file_path)
        #plt.close(fig)


        return model, future#, file_path

    # Evaluate prediction model for one year
    def evaluate_prediction(self, start_date=None, end_date=None, nshares = None, ax = None):

        # Default start date is one year before end of data
        # Default end date is end date of data
        details_dict = {}
        if start_date is None:
            start_date = self.max_date - pd.DateOffset(years=1)
        if end_date is None:
            end_date = self.max_date

        start_date, end_date = self.handle_dates(start_date, end_date)

        # Training data starts self.training_years years before start date and goes up to start date
        train = self.stock[(self.stock['Date'] < start_date) &
                           (self.stock['Date'] > (start_date - pd.DateOffset(years=self.training_years)))]

        # Testing data is specified in the range
        test = self.stock[(self.stock['Date'] >= start_date) & (self.stock['Date'] <= end_date)]

        # Create and train the model
        model = self.create_model()
        model.fit(train)

        # Make a future dataframe and predictions
        future = model.make_future_dataframe(periods = 365, freq='D')
        future = model.predict(future)

        # Merge predictions with the known values
        test = pd.merge(test, future, on = 'ds', how = 'inner')

        train = pd.merge(train, future, on = 'ds', how = 'inner')

        # Calculate the differences between consecutive measurements
        test['pred_diff'] = test['yhat'].diff()
        test['real_diff'] = test['y'].diff()

        # Correct is when we predicted the correct direction
        test['correct'] = (np.sign(test['pred_diff'][1:]) == np.sign(test['real_diff'][1:])) * 1

        # Accuracy when we predict increase and decrease
        increase_accuracy = 100 * np.mean(test[test['pred_diff'] > 0]['correct'])
        decrease_accuracy = 100 * np.mean(test[test['pred_diff'] < 0]['correct'])

        # Calculate mean absolute error
        test_errors = abs(test['y'] - test['yhat'])
        test_mean_error = np.mean(test_errors)

        train_errors = abs(train['y'] - train['yhat'])
        train_mean_error = np.mean(train_errors)

        # Calculate percentage of time actual value within prediction range
        test['in_range'] = False

        for i in test.index:
            if (test.loc[i, 'y'] < test.loc[i, 'yhat_upper']) & (test.loc[i, 'y'] > test.loc[i, 'yhat_lower']):
                test.loc[i, 'in_range'] = True

        in_range_accuracy = 100 * np.mean(test['in_range'])

        if not nshares:

            # Date range of predictions
            print('\nPrediction Range: {} to {}.'.format(start_date,
                end_date))
            details_dict['Prediction Range'] = '{} to {}.'.format(start_date, end_date)
            # Final prediction vs actual value
            print('\nPredicted price on {} = ${:.2f}.'.format(max(future['ds']), future.loc[future.index[-1], 'yhat']))
            details_dict['Predicted price on'] = '{} = ${:.2f}.'.format(max(future['ds']), future.loc[future.index[-1], 'yhat'])
            print('Actual price on    {} = ${:.2f}.\n'.format(max(test['ds']), test.loc[test.index[-1], 'y']))
            details_dict['Actual price on'] = '{} = ${:.2f}.\n'.format(max(test['ds']), test.loc[test.index[-1], 'y'])
            print('Average Absolute Error on Training Data = ${:.2f}.'.format(train_mean_error))
            details_dict['Average Absolute Error on Training Data'] = '${:.2f}.'.format(train_mean_error)
            print('Average Absolute Error on Testing  Data = ${:.2f}.\n'.format(test_mean_error))
            details_dict['Average Absolute Error on Testing  Data'] = '${:.2f}.\n'.format(test_mean_error)
            # Direction accuracy
            print('When the model predicted an increase, the price increased {:.2f}% of the time.'.format(increase_accuracy))
            details_dict['When the model predicted an increase, the price increased'] = '{:.2f}% of the time.'.format(increase_accuracy)
            print('When the model predicted a  decrease, the price decreased  {:.2f}% of the time.\n'.format(decrease_accuracy))
            details_dict['The actual value was within the '] = '{:d}% confidence interval {:.2f}% of the time.'.format(int(100 * model.interval_width), in_range_accuracy)
            print('The actual value was within the {:d}% confidence interval {:.2f}% of the time.'.format(int(100 * model.interval_width), in_range_accuracy))


            # Reset the plot
            # self.reset_plot()

            # Set up the plot
            # fig, ax = plt.subplots(1, 1)

            # Plot the actual values
            ax.plot(train['ds'], train['y'], 'ko-', linewidth = 1.4, alpha = 0.8, ms = 1.8, label = 'Observations')
            ax.plot(test['ds'], test['y'], 'ko-', linewidth = 1.4, alpha = 0.8, ms = 1.8, label = 'Observations')

            # Plot the predicted values
            ax.plot(future['ds'], future['yhat'], 'navy', linewidth = 2.4, label = 'Predicted')

            # Plot the uncertainty interval as ribbon
            ax.fill_between(future['ds'].dt.to_pydatetime(), future['yhat_upper'], future['yhat_lower'], alpha = 0.6,
                           facecolor = 'gold', edgecolor = 'k', linewidth = 1.4, label = 'Confidence Interval')

            # Put a vertical line at the start of predictions
            ax.vlines(x=min(test['ds']), ymin=min(future['yhat_lower']), ymax=max(future['yhat_upper']), colors = 'r',
                       linestyles='dashed', label = 'Prediction Start')

            # Plot formatting
            ax.legend(loc = 2, prop={'size': 8})
            plt.xlabel('Date')
            plt.ylabel('Price $')
            ax.grid(linewidth=0.6, alpha = 0.6)

            ax.set_title('{} Model Evaluation from {} to {} - CPS {}.'.format(self.symbol,
                start_date, end_date, self.changepoint_prior_scale))
            # plt.show();


        # If a number of shares is specified, play the game
        elif nshares:

            # Only playing the stocks when we predict the stock will increase
            test_pred_increase = test[test['pred_diff'] > 0]

            test_pred_increase.reset_index(inplace=True)
            prediction_profit = []

            # Iterate through all the predictions and calculate profit from playing
            for i, correct in enumerate(test_pred_increase['correct']):

                # If we predicted up and the price goes up, we gain the difference
                if correct == 1:
                    prediction_profit.append(nshares * test_pred_increase.loc[i, 'real_diff'])
                # If we predicted up and the price goes down, we lose the difference
                else:
                    prediction_profit.append(nshares * test_pred_increase.loc[i, 'real_diff'])

            test_pred_increase['pred_profit'] = prediction_profit

            # Put the profit into the test dataframe
            test = pd.merge(test, test_pred_increase[['ds', 'pred_profit']], on = 'ds', how = 'left')
            test.loc[0, 'pred_profit'] = 0

            # Profit for either method at all dates
            test['pred_profit'] = test['pred_profit'].cumsum().ffill()
            test['hold_profit'] = nshares * (test['y'] - float(test.loc[0, 'y']))

            # Display information
            print('You played the stock market in {} from {} to {} with {} shares.\n'.format(
                self.symbol, start_date, end_date, nshares))

            print('When the model predicted an increase, the price increased {:.2f}% of the time.'.format(increase_accuracy))
            print('When the model predicted a  decrease, the price decreased  {:.2f}% of the time.\n'.format(decrease_accuracy))

            # Display some friendly information about the perils of playing the stock market
            print('The total profit using the Prophet model = ${:.2f}.'.format(np.sum(prediction_profit)))
            print('The Buy and Hold strategy profit =         ${:.2f}.'.format(float(test.loc[test.index[-1], 'hold_profit'])))
            print('\nThanks for playing the stock market!\n')



            # Plot the predicted and actual profits over time
            # self.reset_plot()

            # Final profit and final smart used for locating text
            final_profit = test.loc[test.index[-1], 'pred_profit']
            final_smart = test.loc[test.index[-1], 'hold_profit']

            # text location
            last_date = test.loc[test.index[-1], 'ds']
            text_location = (last_date - pd.DateOffset(months = 1))

            # Plot smart profits
            plt.plot(test['ds'], test['hold_profit'], 'b',
                     linewidth = 1.8, label = 'Buy and Hold Strategy')

            # Plot prediction profits
            plt.plot(test['ds'], test['pred_profit'],
                     color = 'g' if final_profit > 0 else 'r',
                     linewidth = 1.8, label = 'Prediction Strategy')

            # Display final values on graph
            plt.text(x = text_location,
                     y =  final_profit + (final_profit / 40),
                     s = '$%d' % final_profit,
                    color = 'g' if final_profit > 0 else 'r',
                    size = 18)

            plt.text(x = text_location,
                     y =  final_smart + (final_smart / 40),
                     s = '$%d' % final_smart,
                    color = 'g' if final_smart > 0 else 'r',
                    size = 18)

            # Plot formatting
            plt.ylabel('Profit  (US $)'); plt.xlabel('Date')
            plt.title('Predicted versus Buy and Hold Profits')
            plt.legend(loc = 2, prop={'size': 10})
            plt.grid(alpha=0.2)
            # plt.show()

        # file_path = helper.util.get_temp_file()
        # fig.savefig(file_path)
        # plt.close(fig)
        return details_dict
        # return file_path

    def retrieve_google_trends(self, search, date_range):

        # Set up the trend fetching object
        pytrends = TrendReq(hl='en-US', tz=360)
        kw_list = [search]

        try:

            # Create the search object
            pytrends.build_payload(kw_list, cat=0, timeframe=date_range[0], geo='', gprop='news')

            # Retrieve the interest over time
            trends = pytrends.interest_over_time()

            related_queries = pytrends.related_queries()

        except Exception as e:
            print('\nGoogle Search Trend retrieval failed.')
            print(e)
            return

        return trends, related_queries

    def changepoint_date_analysis(self, search=None):
        # self.reset_plot()

        model = self.create_model()

        # Use past self.training_years years of data
        train = self.stock[self.stock['Date'] > (self.max_date - pd.DateOffset(years = self.training_years))]
        model.fit(train)

        # Predictions of the training data (no future periods)
        future = model.make_future_dataframe(periods=0, freq='D')
        future = model.predict(future)

        train = pd.merge(train, future[['ds', 'yhat']], on = 'ds', how = 'inner')

        changepoints = model.changepoints
        train = train.reset_index(drop=True)

        # Create dataframe of only changepoints
        change_indices = []
        for changepoint in (changepoints):
            change_indices.append(train[train['ds'] == changepoint].index[0])

        c_data = train.loc[change_indices, :]
        deltas = model.params['delta'][0]

        c_data['delta'] = deltas
        c_data['abs_delta'] = abs(c_data['delta'])

        # Sort the values by maximum change
        c_data = c_data.sort_values(by='abs_delta', ascending=False)

        # Limit to 10 largest changepoints
        c_data = c_data[:10]

        # Separate into negative and positive changepoints
        cpos_data = c_data[c_data['delta'] > 0]
        cneg_data = c_data[c_data['delta'] < 0]

        # Changepoints and data
        if not search:

            print('\nChangepoints sorted by slope rate of change (2nd derivative):\n')
            print(c_data.loc[:, ['Date', 'Adj. Close', 'delta']][:5])

            # Line plot showing actual values, estimated values, and changepoints
            # self.reset_plot()

            # Set up line plot
            plt.plot(train['ds'], train['y'], 'ko', ms = 4, label = 'Stock Price')
            plt.plot(future['ds'], future['yhat'], color = 'navy', linewidth = 2.0, label = 'Modeled')

            # Changepoints as vertical lines
            plt.vlines(cpos_data['ds'].dt.to_pydatetime(), ymin = min(train['y']), ymax = max(train['y']),
                       linestyles='dashed', color = 'r',
                       linewidth= 1.2, label='Negative Changepoints')

            plt.vlines(cneg_data['ds'].dt.to_pydatetime(), ymin = min(train['y']), ymax = max(train['y']),
                       linestyles='dashed', color = 'darkgreen',
                       linewidth= 1.2, label='Positive Changepoints')

            plt.legend(prop={'size':10});
            plt.xlabel('Date'); plt.ylabel('Price ($)'); plt.title('Stock Price with Changepoints')
            plt.show()

        # Search for search term in google news
        # Show related queries, rising related queries
        # Graph changepoints, search frequency, stock price
        if search:
            date_range = ['%s %s' % (str(min(train['Date'])), str(max(train['Date'])))]

            # Get the Google Trends for specified terms and join to training dataframe
            trends, related_queries = self.retrieve_google_trends(search, date_range)

            if (trends is None)  or (related_queries is None):
                print('No search trends found for %s' % search)
                return

            print('\n Top Related Queries: \n')
            print(related_queries[search]['top'].head())

            print('\n Rising Related Queries: \n')
            print(related_queries[search]['rising'].head())

            # Upsample the data for joining with training data
            trends = trends.resample('D')

            trends = trends.reset_index(level=0)
            trends = trends.rename(columns={'date': 'ds', search: 'freq'})

            # Interpolate the frequency
            trends['freq'] = trends['freq'].interpolate()

            # Merge with the training data
            train = pd.merge(train, trends, on = 'ds', how = 'inner')

            # Normalize values
            train['y_norm'] = train['y'] / max(train['y'])
            train['freq_norm'] = train['freq'] / max(train['freq'])

            # self.reset_plot()

            # Plot the normalized stock price and normalize search frequency
            plt.plot(train['ds'], train['y_norm'], 'k-', label = 'Stock Price')
            plt.plot(train['ds'], train['freq_norm'], color='goldenrod', label = 'Search Frequency')

            # Changepoints as vertical lines
            plt.vlines(cpos_data['ds'].dt.to_pydatetime(), ymin = 0, ymax = 1,
                       linestyles='dashed', color = 'r',
                       linewidth= 1.2, label='Negative Changepoints')

            plt.vlines(cneg_data['ds'].dt.to_pydatetime(), ymin = 0, ymax = 1,
                       linestyles='dashed', color = 'darkgreen',
                       linewidth= 1.2, label='Positive Changepoints')

            # Plot formatting
            plt.legend(prop={'size': 10})
            plt.xlabel('Date'); plt.ylabel('Normalized Values'); plt.title('%s Stock Price and Search Frequency for %s' % (self.symbol, search))
            plt.show()

    # Predict the future price for a given range of days
    def predict_future(self, days=30, ax = None):

        # Use past self.training_years years for training
        train = self.stock[self.stock['Date'] > (max(self.stock['Date']) - pd.DateOffset(years=self.training_years))]

        model = self.create_model()

        model.fit(train)

        # Future dataframe with specified number of days to predict
        future = model.make_future_dataframe(periods=days, freq='D')
        future = model.predict(future)

        # Only concerned with future dates
        future = future[future['ds'] >= max(self.stock['Date'])]

        # Remove the weekends
        future = self.remove_weekends(future)

        # Calculate whether increase or not
        future['diff'] = future['yhat'].diff()

        future = future.dropna()

        # Find the prediction direction and create separate dataframes
        future['direction'] = (future['diff'] > 0) * 1

        # Rename the columns for presentation
        future = future.rename(columns={'ds': 'Date', 'yhat': 'estimate', 'diff': 'change',
                                        'yhat_upper': 'upper', 'yhat_lower': 'lower'})

        future_increase = future[future['direction'] == 1]
        future_decrease = future[future['direction'] == 0]

        # Print out the dates
        print('\nPredicted Increase: \n')
        print(future_increase[['Date', 'estimate', 'change', 'upper', 'lower']])

        print('\nPredicted Decrease: \n')
        print(future_decrease[['Date', 'estimate', 'change', 'upper', 'lower']])

        # self.reset_plot()

        # Set up plot
        # plt.style.use('fivethirtyeight')
        # matplotlib.rcParams['axes.labelsize'] = 10
        # matplotlib.rcParams['xtick.labelsize'] = 8
        # matplotlib.rcParams['ytick.labelsize'] = 8
        # matplotlib.rcParams['axes.titlesize'] = 12

        # Plot the predictions and indicate if increase or decrease
        # fig, ax = plt.subplots(1, 1, figsize=(8, 6))

        # Plot the estimates
        ax.plot(future_increase['Date'], future_increase['estimate'], 'g^', ms = 12, label = 'Pred. Increase')
        ax.plot(future_decrease['Date'], future_decrease['estimate'], 'rv', ms = 12, label = 'Pred. Decrease')

        # Plot errorbars
        ax.errorbar(future['Date'].dt.to_pydatetime(), future['estimate'],
                    yerr = future['upper'] - future['lower'],
                    capthick=1.4, color = 'k',linewidth = 2,
                   ecolor='darkblue', capsize = 4, elinewidth = 1, label = 'Pred with Range')

        # Plot formatting
        ax.legend(loc = 2, prop={'size': 10})
        #plt.xticks(rotation = '45')
        plt.ylabel('Predicted Stock Price (US $)')
        plt.xlabel('Date')
        ax.set_title('Predictions for %s' % self.symbol)
        # plt.show()

        # file_path = helper.util.get_temp_file()
        # fig.savefig(file_path)
        # plt.close(fig)

        # return file_path

    def changepoint_prior_validation(self, start_date=None, end_date=None, changepoint_priors = [0.001, 0.05, 0.1, 0.2], ax1 = None, ax2 = None, ax3 = None):


        # Default start date is two years before end of data
        # Default end date is one year before end of data
        if start_date is None:
            start_date = self.max_date - pd.DateOffset(years=2)
        if end_date is None:
            end_date = self.max_date - pd.DateOffset(years=1)

        # Convert to pandas datetime for indexing dataframe
        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)

        start_date, end_date = self.handle_dates(start_date, end_date)

        # Select self.training_years number of years
        train = self.stock[(self.stock['Date'] > (start_date - pd.DateOffset(years=self.training_years))) &
        (self.stock['Date'] < start_date)]

        # Testing data is specified by range
        test = self.stock[(self.stock['Date'] >= start_date) & (self.stock['Date'] <= end_date)]

        eval_days = (max(test['Date']) - min(test['Date'])).days

        results = pd.DataFrame(0, index = list(range(len(changepoint_priors))),
            columns = ['cps', 'train_err', 'train_range', 'test_err', 'test_range'])

        print('\nValidation Range {} to {}.\n'.format(min(test['Date']),
            max(test['Date'])))


        # Iterate through all the changepoints and make models
        for i, prior in enumerate(changepoint_priors):
            results.loc[i, 'cps'] = prior

            # Select the changepoint
            self.changepoint_prior_scale = prior

            # Create and train a model with the specified cps
            model = self.create_model()
            model.fit(train)
            future = model.make_future_dataframe(periods=eval_days, freq='D')

            future = model.predict(future)

            # Training results and metrics
            train_results = pd.merge(train, future[['ds', 'yhat', 'yhat_upper', 'yhat_lower']], on = 'ds', how = 'inner')
            avg_train_error = np.mean(abs(train_results['y'] - train_results['yhat']))
            avg_train_uncertainty = np.mean(abs(train_results['yhat_upper'] - train_results['yhat_lower']))

            results.loc[i, 'train_err'] = avg_train_error
            results.loc[i, 'train_range'] = avg_train_uncertainty

            # Testing results and metrics
            test_results = pd.merge(test, future[['ds', 'yhat', 'yhat_upper', 'yhat_lower']], on = 'ds', how = 'inner')
            avg_test_error = np.mean(abs(test_results['y'] - test_results['yhat']))
            avg_test_uncertainty = np.mean(abs(test_results['yhat_upper'] - test_results['yhat_lower']))

            results.loc[i, 'test_err'] = avg_test_error
            results.loc[i, 'test_range'] = avg_test_uncertainty

        results = results.round(3)
        print(results)
        model_efficiency_df = results # pd.DataFrame.from_dict(results, orient='index')
        font_size = 14
        bbox = [0, 0, 1, 1]
        ax3.axis('off')
        mpl_table = ax3.table(cellText=model_efficiency_df.values, rowLabels=model_efficiency_df.index, bbox=bbox, colLabels=model_efficiency_df.columns)
        mpl_table.auto_set_font_size(False)
        mpl_table.set_fontsize(font_size)
        ax3.set_title("CPS Efficiency: %s"%('Validation Range {} to {}.\n'.format(min(test['Date']), max(test['Date']))))


        # Plot of training and testing average errors
        # self.reset_plot()

        ax1.plot(results['cps'], results['train_err'], 'bo-', ms = 8, label = 'Train Error')
        ax1.plot(results['cps'], results['test_err'], 'r*-', ms = 8, label = 'Test Error')
        ax1.set_xlabel('Changepoint Prior Scale')
        ax1.set_ylabel('Avg. Absolute Error ($)')
        ax1.set_title('Training and Testing Curves as Function of CPS')
        ax1.grid(color='k', alpha=0.3)
        # ax1.set_xticks(results['cps'], results['cps'])
        ax1.legend(prop={'size':10})
        # plt.show();

        # file_path = helper.util.get_temp_file()
        # plt.savefig(file_path)


        # Plot of training and testing average uncertainty
        # self.reset_plot()

        ax2.plot(results['cps'], results['train_range'], 'bo-', ms = 8, label = 'Train Range')
        ax2.plot(results['cps'], results['test_range'], 'r*-', ms = 8, label = 'Test Range')
        ax2.set_xlabel('Changepoint Prior Scale')
        ax2.set_ylabel('Avg. Uncertainty ($)')
        ax2.set_title('Uncertainty in Estimate as Function of CPS')
        ax2.grid(color='k', alpha=0.3)
        # ax2.set_xticks(results['cps'], results['cps'])
        ax2.legend(prop={'size':10})
        # plt.show()

        # file_path = helper.util.get_temp_file()
        # plt.savefig(file_path)