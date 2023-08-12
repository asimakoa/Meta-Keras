# -*- coding: utf-8 -*-
"""
Created on Sat Aug 12 13:32:13 2023

@author: Nassos
"""


Conversation opened. 1 unread message.

Skip to content
Using Gmail with screen readers
1 of 14,907
asdf
Inbox

Assimakopoulos Athanassios
Attachments
1:31 PM (0 minutes ago)
to me

# -*- coding: utf-8 -*-

"""

Created on Wed Aug  9 17:36:35 2023

 

@author: nassos.asimakopoulos

"""

 

import pandas as pd

import os

 

 

#df_10_1M=df_10_1M[["<DATE>", "<TIME>", "open", "high", "low", "close", "<TICKVOL>", "<VOL>", "<SPREAD>"]]

 

 

df= pd.read_csv(r'F:\\Dealing\\TRADING\\Fenix\\FMD_FXO_20230630_TICK.csv')

df.columns = df.iloc[0]

df = df.iloc[1:]

df = df.reset_index().set_index('Time')

df = df.drop('index', axis=1)

 

 

 

# Drop rows with NaN values in the 'Tenor' column

df = df.dropna(subset=['Tenor'])

# Get unique values from the cleaned 'Tenor' column

UniqueTenors = df['Tenor'].unique()

UniqueTypes = df['PriceType'].unique()

 

for Tenor in UniqueTenors:

    for PriceType in UniqueTypes:

 

        df_TenorType=df[(df['Tenor']== Tenor)&(df['PriceType']== PriceType)]

       

        

        

        # Convert 'Mid', 'Bid', and 'Ask' columns to numeric types

        numeric_columns = ['Mid', 'Bid', 'Ask']

       

        df_TenorType[numeric_columns] = df_TenorType[numeric_columns].apply(pd.to_numeric)

   

        # Convert the index to DatetimeIndex

        df_TenorType.index = pd.to_datetime(df_TenorType.index)

       

    

    

        # Apply both forward-fill and backward-fill to fill missing values before resampling

        df_TenorType = df_TenorType[numeric_columns].fillna(method='ffill').fillna(method='bfill')

   

        # Resample tick data to minute data using OHLC for numeric columns

       

        df_TenorType = df_TenorType['Mid'].resample('1T').ohlc().ffill().bfill()

   

    

    

    

        df_TenorType.rename(columns={'open': '<OPEN>'}, inplace=True)

       df_TenorType.rename(columns={'high': '<HIGH>'}, inplace=True)

        df_TenorType.rename(columns={'low': '<LOW>'}, inplace=True)

        df_TenorType.rename(columns={'close': '<CLOSE>'}, inplace=True)   

        df_TenorType['<TICKVOL>'] = 1

        df_TenorType['<VOL>'] = 1

        df_TenorType['<SPREAD>'] = 1

        df_TenorType['<DATE>'] = df_TenorType.index.date

        df_TenorType['<TIME>'] = df_TenorType.index.time

        df_TenorType=df_TenorType[["<DATE>", "<TIME>", "<OPEN>", "<HIGH>", "<LOW>", "<CLOSE>", "<TICKVOL>", "<VOL>", "<SPREAD>"]]

       

        

        

        

        print(df_TenorType)

        file_prefix = f'{Tenor}_{PriceType}.csv'

        output_filename = f'{file_prefix}.csv'

        # Use the parameterized filename to save the DataFrame to a CSV file

        df_TenorType.to_csv(f'F:\\Dealing\\TRADING\\Fenix\\NassosCSV\\{output_filename}', index=False)

   

    

 

Nassos Asimakopoulos
Derivatives and FX Trading Desk, Markets & Asset Management

 


Eurobank-Logokit-RGB 


EUROBANK S.A.
8 Othonos Str.

10557 Athens
t. +30 210 3718987 (28987))
m. +30 6945958083

 

 

P Think before you print.


Disclaimer:
This e-mail is confidential. If you are not the intended recipient, you should not copy it, re-transmit it, use it or disclose its contents, but should return it to the sender immediately and delete the copy from your system.
Eurobank S.A. is not responsible for, nor endorses, any opinion, recommendation, conclusion, solicitation, offer or agreement or any information contained in this communication.
Eurobank S.A. cannot accept any responsibility for the accuracy or completeness of this message as it has been transmitted over a public network. If you suspect that the message may have been intercepted or amended, please call the sender.


 One attachment
  •  Scanned by Gmail
