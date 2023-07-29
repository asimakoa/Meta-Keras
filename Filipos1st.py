# -*- coding: utf-8 -*-
"""
Created on Mon Jul 24 16:58:42 2023
@author: Nassos
"""

import pandas as pd
import numpy as np
import MetaTrader5 as mt5
import datetime  # Import the datetime module
from keras.models import Sequential
from keras.layers import LSTM, Dense
from sklearn.model_selection import train_test_split

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
timeframe = mt5.TIMEFRAME_M1   # Daily timeframe

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
        df.set_index('time', inplace=True)
        Prices=df['close']

        # Print the historical data
        print(df)
    else:
        print("DataFrame is empty. No historical data retrieved.")
else:
    print("Data retrieval failed. Please check the symbol and timeframe.")

# Shutdown the MetaTrader 5 connection
mt5.shutdown()


# Assuming Prices is the Series containing the 'close' prices with timestamps as the index
# Make sure the data is sorted by the timestamp
Prices.sort_index(inplace=True)

# Convert the Prices Series to a numpy array
data = Prices.values.reshape(-1, 1)

# Normalize the data (optional but can be helpful for some neural networks)
data_normalized = data / np.max(data) #we normalize between 0 and 1.

# Define the sequence length for input data (e.g., 10 timestamps as input for each sample)
sequence_length = 10 #I input 10 prices and the label is the 11th.

# Prepare the sequences and labels for training
sequences = []
labels = []
for i in range(len(data_normalized) - sequence_length):
    sequences.append(data_normalized[i:i + sequence_length])
    labels.append(data_normalized[i + sequence_length])

# Convert the sequences and labels to numpy arrays
sequences = np.array(sequences)
labels = np.array(labels)

# Split the data into training and evaluation sets (80% training, 20% evaluation)
X_train, X_eval, y_train, y_eval = train_test_split(sequences, labels, test_size=0.2, random_state=42)

# Create the LSTM model
model = Sequential()
model.add(LSTM(50, activation='relu', input_shape=(sequence_length, 1)))
model.add(Dense(1))
model.compile(optimizer='adam', loss='mean_squared_error')

# Train the model
model.fit(X_train, y_train, epochs=5, batch_size=32, validation_data=(X_eval, y_eval))


# Evaluate the model on the evaluation set
evaluation_loss = model.evaluate(X_eval, y_eval)

# Predict now. Evaluation is like a safe predict. The backtesting is the evaluation.

# Print the evaluation loss (MSE or RMSE, depending on the model's loss function)
print("Evaluation Loss:", evaluation_loss)

# Save the model to a file named 'my_model.h5'
model.save('my_1st_model.h5')


