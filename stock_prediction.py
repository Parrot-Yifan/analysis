#some note for prophet
#the prophet itself takes a csv file only contains two parameter 'ds' and 'y'
#'ds' is the date, in the form of '2024-02-16'
#'y' is the value already exist and we want to predict
#current problem: yfinance can only return data from one day ago after the market closes for the day, which means that if today is the 25th, you have to wait until 9pm gmt to access the data from the 24th!
from prophet import Prophet
import yfinance as yf
import pandas as pd
from supabase import create_client, Client
from datetime import datetime, timedelta
from db_interaction import *


def main_stock_prediction_function():

    # Write logic for the main stock prediction function.

    # First obtain all tickers. 
    tickers = get_tickers()

    for ticker in tickers:
        prediction, datetime = forecast_5min(ticker)
        remove_existing_company_stock(ticker)
        insert_company_stock(ticker, prediction, datetime)

# def forecast_5min(ticker):
#     df = yf.download(tickers = ticker, period='10d', interval = '5m')
#     df.reset_index(inplace=True)
#     df['Datetime'] = pd.to_datetime(df['Datetime']).apply(lambda x: x.replace(tzinfo=None))
#     df.rename(columns={'Datetime': 'ds', 'Close': 'y'}, inplace=True)
#     df = df[['ds','y']]
#     m = Prophet()
#     m.fit(df)
#     future = m.make_future_dataframe(periods=96, freq='5min')  #next 96/12 hours
#     forecast = m.predict(future)

#     # Get the current date and time
#     current_time = datetime.now()

#     # Calculate the time 5 minutes from now
#     time_in_5_minutes = current_time + timedelta(minutes=5)

#     # Filter forecast data for the time in 5 minutes
#     future_data_5_minutes = forecast[pd.to_datetime(forecast['ds']) == time_in_5_minutes][['ds', 'yhat']]
#     # fig2.savefig('forcast_components.png')

#     # Extract prediction value and datetime
#     if not future_data_5_minutes.empty:
#         prediction_value = future_data_5_minutes['yhat'].iloc[0]
#         datetime_value = future_data_5_minutes['ds'].iloc[0]
        
#         print(f"Prediction Value at {datetime_value}: {prediction_value}")
#         return prediction_value, datetime_value
#     else:
#         print("No data found for the specified time.")
#         return None, None

def forecast_5min(ticker):
    df = yf.download(tickers = ticker, period='10d', interval = '5m')
    df.reset_index(inplace=True)
    df['Datetime'] = pd.to_datetime(df['Datetime']).apply(lambda x: x.replace(tzinfo=None))
    df.rename(columns={'Datetime': 'ds', 'Close': 'y'}, inplace=True)
    df = df[['ds','y']]
    m = Prophet()
    m.fit(df)
    future = m.make_future_dataframe(periods=384, freq='5min')  #next 96/12 hours
    forecast = m.predict(future)
    forecast = forecast[(forecast['ds'].dt.time >= pd.to_datetime('09:30:00').time()) & (forecast['ds'].dt.time <= pd.to_datetime('16:00:00').time())]
    forecast['ds'] = pd.to_datetime(forecast['ds'])
    now = datetime.now()
    nasdaq_open = time(9, 30)  
    nasdaq_close = time(16, 0) 
    now = datetime.now().astimezone(tz=datetime.now().astimezone().tzinfo)
    current_time = now.time()
    if not nasdaq_open <= current_time <= nasdaq_close:
        return
    else:
        next_5_min = now + timedelta(minutes=(5 - now.minute % 5), seconds=-now.second, microseconds=-now.microsecond)
        next_5_min_data = forecast[forecast['ds'] == next_5_min.strftime('%Y-%m-%d %H:%M:%S')]
        time = next_5_min_data['ds'].tolist()
        timestamp = [int(ts.timestamp()) for ts in time]
        yhat = next_5_min_data['yhat'].tolist()

    return timestamp[0],yhat[0]


# data=yf.download(tickers = 'AAPL', period='1d', interval = '5m')
# data.reset_index(inplace=True)
# data['Datetime'] = pd.to_datetime(data['Datetime']).apply(lambda x: x.replace(tzinfo=None))
# data.rename(columns={'Datetime': 'ds', 'Close': 'y'}, inplace=True)
# print(data)
