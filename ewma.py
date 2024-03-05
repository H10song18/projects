#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pandas as pd
import pickle
import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt

def loadTSData(ticker, sd, ed):
    filename = ticker + "_" + sd + "_" + ed + ".pickle"
    try:
        with open(filename, 'rb') as f:
            data = pickle.load(f)
        f.close()
        print("Loaded data.")
    except (OSError, IOError) as e:
        data = yf.download(ticker, sd, ed)
        with open(filename+'.pickle', 'wb') as f:
            pickle.dump(data, f)
        f.close()
        print("Downloaded data.")
    return data
        
ticker = 'CHFPLN=X'
startdate = '2020-12-31'
enddate = '2023-10-01'
    

ts_data = loadTSData(ticker, startdate, enddate)['Close'].reset_index()
ts_data['Date'] = pd.to_datetime(ts_data['Date']).dt.normalize()       
    

# # Sample historical return data (replace this with your own dataset)
ts_data['Pct_Chg'] = ts_data['Close'].pct_change(1)
ts_data['Return'] = np.log(ts_data['Close']).diff()
                            
          
returns = ts_data['Return'].dropna().tolist()
# Define the smoothing parameter (lambda)
lambda_value = 0.94  # You can adjust this value based on your preferences

# Calculate the initial EWMA volatility (assuming an initial window of 5 periods)
initial_window = 5
initial_volatility = pd.Series(returns[:initial_window]).var()

# Initialize lists to store EWMA volatility and EWMA values
ewma_volatility = [initial_volatility]
ewma_values = [initial_volatility]

# Calculate EWMA volatility for each subsequent period
for i in range(initial_window, len(returns)):
    ewma_value = lambda_value * (returns[i] - ewma_values[-1]) ** 2 + (1 - lambda_value) * ewma_values[-1]
    ewma_volatility.append(ewma_value)
    ewma_values.append(ewma_value)

# Convert the result into a pandas DataFrame for further analysis
result_df = pd.DataFrame({'Returns': returns[initial_window-1:], 'EWMA_Volatility': ewma_volatility})

print(result_df)
plt.figure(figsize=(10, 6))
plt.plot(result_df['Returns'], label='Returns', marker='o')
plt.plot(result_df['EWMA_Volatility'], label='EWMA Volatility', linestyle='--', marker='o')
plt.title('EWMA Volatility Estimation')
plt.xlabel('Time Period')
plt.ylabel('Value')
plt.legend()
plt.grid(True)
plt.show()