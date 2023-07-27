# -*- coding: utf-8 -*-
"""
Created on Mon Jul 24 16:58:42 2023
@author: Nassos
"""

import pandas as pd
import MetaTrader5 as mt5
import datetime  # Import the datetime module

path = "C:\\Program Files\\MetaTrader 5\\terminal64.exe"  # Path to the MetaTrader 5 terminal EXE file
login = 7030050                   # Account number
password = "trrq3qxr"             # Password
server = "BlueberryMarkets-Demo"         # Server name as it is specified in the terminal
timeout = 10000                   # Timeout (replace 10000 with your desired timeout value)
portable = False                  # Portable mode

mt5.initialize(
    path=path,
    login=login,
    password=password,
    server=server,
    timeout=timeout,
    portable=portable
)

# Define the symbol and timeframe for data retrieval
symbol = "EURUSD"       # EUR/USD symbol
timeframe = mt5.TIMEFRAME_D1   # Daily timeframe

# Specify the start and end time for data retrieval
start_time = datetime.datetime(2022, 1, 1)
end_time = datetime.datetime(2022, 12, 12)

# Request historical data
rates = mt5.copy_rates_range(symbol, timeframe, start_time, end_time)

# Check if data retrieval is successful
if rates is not None:
    # Convert the data to a pandas DataFrame for easier manipulation
    df = pd.DataFrame(rates)

    # Check if the DataFrame is empty
    if not df.empty:
        # Convert the timestamp to a human-readable format
        df['time'] = pd.to_datetime(df['time'], unit='s')

        # Print the historical data
        print(df)
    else:
        print("DataFrame is empty. No historical data retrieved.")
else:
    print("Data retrieval failed. Please check the symbol and timeframe.")

# Shutdown the MetaTrader 5 connection
mt5.shutdown()