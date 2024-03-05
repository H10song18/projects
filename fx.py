#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import yfinance as yf
import pandas as pd
import numpy as np
import pickle
import matplotlib.pyplot as plt
import datetime as dt
from statsmodels.tsa.stattools import adfuller
from arch import arch_model
import statsmodels.tsa.api as smt
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf

ticker = 'GBPUSD=X'
#ticker = 'EURUSD=X'
startdate = '2018-03-30'
enddate = '2021-03-30'
filename = ticker + "_" + startdate + "_" + enddate

def loadData():
    try:
        with open(filename, 'rb') as f:
            data = pickle.load(f)
        f.close()
        print("Loaded data.")
        
    except (OSError, IOError) as e:
        data = yf.download(ticker, startdate, enddate)
        with open(filename, 'wb') as f:
            pickle.dump(data, f)
        f.close()
        print("Downloaded data.")
    
    return data
        
def perform_adf_test(series):
    result = adfuller(series)
    print('ADF Statistic: %f' % result[0])
    print('p-value: %f' % result[1])
    print('Stationary' if result[1] < 0.05 else 'Non-Stationary')
       
def plotSeries(series, title=None):
    plt.figure()
    plt.plot(series)
    plt.title(title)
    
    plot_acf(series)
    plot_pacf(series)

def getReturns(ts):
    returns = ts[['Date', 'Adj Close']]
    returns = returns.set_index('Date')
    returns['Returns'] = returns['Adj Close'].pct_change()*100
    returns = returns.dropna().drop('Adj Close', axis=1)
    
    return returns

def getBestOrder(ts):
    best_aic = np.inf 
    best_order = None
    best_mdl = None
    
    rng = range(10)
    for p in rng:
        for q in rng:
            try:
                tmp_mdl = smt.ARMA(ts, order=(p, q)).fit(method='mle', trend='nc')
                tmp_aic = tmp_mdl.aic
                if tmp_aic < best_aic:
                    best_aic = tmp_aic
                    best_order = (p, q)
                    best_mdl = tmp_mdl
            except: continue
    
    return best_order

def getModel(ts, test_size, terms=(1, 1)):
    train = ts[:-test_size]
    model = arch_model(train, p=terms[0], q=terms[1])
    model_fit = model.fit(disp='off')
    
    return model_fit
    
def getRollingForecast(ts, test_size, terms=(1, 1)):
    rolling_predictions = []
    
    for i in range(test_size):
        train = ts[:-(test_size-i)]
        model = arch_model(train, p=terms[0], q=terms[1])
        model_fit = model.fit(disp='off')
        pred = model_fit.forecast(horizon=1)
        #rolling_predictions.append(np.sqrt(pred.variance.values[-1,:][0]))
        rolling_predictions.append(pred.mean.values[-1,:][0])
    
    rolling_predictions = pd.Series(rolling_predictions, index=ts.index[-test_size:])
    
    return rolling_predictions

def getSDList(ts):
    sds = [0]
    for i in range(1, len(ts)):
        sds.append(ts[:i].std())
    
    sds = pd.Series(sds, index=ts.index)
    
    return sds

data = loadData()
data['Ticker'] = np.full([len(data.index), 1], ticker)
data = data.reset_index().set_index('Ticker')             
data = data.drop('Volume', axis=1)

ticker_list = data.index.unique()
for t in ticker_list:
    ts = getReturns(data[data.index==t])
    #perform_adf_test(ts)
    #plotSeries(ts)
    
    best_orders = getBestOrder(ts)
    
    test_size = int(0.1*len(ts.index))
    #model = getModel(ts, test_size)
    #print(model.summary())
    
    # model = arch_model(ts, p=1, q=1)    
    # model_fit = model.fit(disp='off')
    # pred = model_fit.forecast(horizon=7)
    # future_dates = [ts.index[-1] + dt.timedelta(days=i) for i in range(1,8)]
    # pred = pd.Series(np.sqrt(pred.variance.values[-1,:]), index=future_dates)
    # plt.plot(pred)
    
    #volList = getSDList(ts)
    
    #forecast = getRollingForecast(ts, test_size)
    #hist, = plt.plot(ts[-test_size:], color='blue')
    #preds, = plt.plot(forecast, color='red')
    
    #model.plot()

    #print(stats.shapiro(model.resid))


#perform_adf_test(returns)

def main():
    pass
    
if __name__ == "__main__":
    main()