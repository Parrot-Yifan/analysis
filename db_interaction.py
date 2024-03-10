from prophet import Prophet
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta,timezone
from db_interaction import *

def main_stock_prediction_function(supabase):
    '''
    The main function for prediction, whcich calls all other functions
    '''
    tickers = get_tickers(supabase)

    for ticker in tickers:
        prediction = forecast_5min(ticker)
        remove_existing_company_stock(ticker,supabase)
        insert_company_stock(ticker, prediction, supabase)


def forecast_5min(ticker):
    '''
    Forecast one ticker for next five minutes
    '''
    #Get the data on yfinance and process it into a format acceptable to prophet
    df = yf.download(tickers = ticker, period='10d', interval = '5m')
    df.reset_index(inplace=True)
    df['Datetime'] = pd.to_datetime(df['Datetime']).apply(lambda x: x.replace(tzinfo=None))
    df.rename(columns={'Datetime': 'ds', 'Close': 'y'}, inplace=True)
    df = df[['ds','y']]

    #Import data into the prophet model and construct a framework for future data, then make predictions
    m = Prophet()
    m.fit(df)
    future = m.make_future_dataframe(periods=768, freq='5min')  #next 768/12=64 hours data
    forecast = m.predict(future)
    forecast['ds'] = pd.to_datetime(forecast['ds'])

    #Filter the data for the next five minutes and convert it into a format acceptable to supabase
    now = datetime.now()
    next_5_min = now + timedelta(minutes=(5 - now.minute % 5), seconds=-now.second, microseconds=-now.microsecond)
    next_5_min_data = forecast[forecast['ds'] == next_5_min.strftime('%Y-%m-%d %H:%M:%S')]
    time = next_5_min_data['ds'].tolist()
    yhat = next_5_min_data['yhat'].tolist()
    return yhat[0]
