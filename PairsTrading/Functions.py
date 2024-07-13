### Library Imports
import yfinance as yf
import pandas as pd
import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")


### Function to Get Commodities Data
def import_commod_data(tickers, start_date, end_date):
    data = pd.DataFrame()
    for t in tickers:
        data[t] = yf.download(t, start = start_date, end = end_date)['Adj Close']
    data = data.replace([np.inf, -np.inf], np.nan).dropna() # Drop nan and inf values
    return data


### Function to Compute Spread and Z-Score
def spread_and_zscore(series1, series2):
    # Calculate the spread between two series
    spread = series1 - series2 
    # Calculate the Z-score of the spread
    z_score = (spread - spread.mean()) / spread.std()  
    return spread, z_score


### Function to check for cointegration
# The cointegration test checks whether there is a long-term equilibrium relationship between the two time series
def check_cointegration(series1, series2):
    # Perform the cointegration test from .coint() function
    result = sm.tsa.stattools.coint(series1, series2)  
    # Extract the p-value from the cointegration test results
    p_val = result[1]  
    return p_val


# Function to Generate Trading Signals
def generate_signals(data, commodities):
    series1 = data[commodities[0]]
    series2 = data[commodities[1]]
    
    spread, z_score = spread_and_zscore(series1, series2)  # Compute spread and Z-score
    
    # Generate trading signals based on Z-score thresholds
    longs = z_score < -1  # Long signal when Z-score is less than -1
    shorts = z_score > 1  # Short signal when Z-score is greater than 1
    exits = abs(z_score) < 0.5  # Exit signal when Z-score is between -0.5 and 0.5
    
    signals = pd.DataFrame(index=data.index)
    signals['longs'] = longs
    signals['shorts'] = shorts
    signals['exits'] = exits
    
    return signals, spread, z_score


### Function to Calculate the position
def backtest(signals, data, commodities):
    # Initialize positions df
    positions = pd.DataFrame(index = signals.index)
    # Initialize positions for the first commodity
    positions[commodities[0]] = 0  
    positions[commodities[1]] = 0  

    for i in range(len(signals)):
        if signals['longs'].iloc[i]:  # Long signal
            total_value = 1000  # Total value to be invested in each position
            positions.iloc[i] = [total_value / data[commodities[0]].iloc[i], -total_value / data[commodities[1]].iloc[i]]
        elif signals['shorts'].iloc[i]:  # Short signal
            total_value = 1000  # Total value to be invested in each position
            positions.iloc[i] = [-total_value / data[commodities[0]].iloc[i], total_value / data[commodities[1]].iloc[i]]
        elif signals['exits'].iloc[i]:  # Exit signal
            positions.iloc[i] = [0, 0]  # Set positions to zero on exit
    
    # Calculate daily returns of the assets
    daily_rets = data.pct_change().dropna()
    # Calculate portfolio returns based on positions and daily returns
    returns = (positions.shift(1) * daily_rets).sum(axis=1)
    # Calculate cumulative returns over the period
    cumulative_rets = (returns + 1).cumprod() - 1

    return positions, returns, cumulative_rets


### Function to Compute Performance Metrics
def calculate_performance_metrics(cumulative_rets, returns):
    # Calculate total return over the period (final value of cumulative returns)
    total_return = cumulative_rets.iloc[-1]
    
    # Calculate total amount return (based on 2000 total invested: 1000 long and 1000 short units)
    total_amount_return = total_return * 2000  # Total return in currency units
    
    # Calculate total percentage return over the period
    percentage_return = total_return * 100
    
    # Calculate the annualized return
    annualized_return = ((1 + total_return) ** (252 / len(cumulative_rets)) - 1) * 100
    
    # Calculate the Sharpe ratio
    sharpe_ratio = returns.mean() / returns.std() * np.sqrt(252)
    
    return total_amount_return, percentage_return, annualized_return, sharpe_ratio


### Plot cumulative returns
def plots(spread, cumulative_rets, z_score):
    plt.figure(figsize = (8, 5))
    plt.plot(cumulative_rets, label = 'Cumulative Returns')
    plt.title('Cumulative Returns')
    plt.xlabel('Date')
    plt.ylabel('Cumulative Returns')
    plt.legend()

    # Plot spread
    plt.figure(figsize = (8, 5))
    plt.plot(spread, label = 'Spread')
    plt.title('Spread')
    plt.xlabel('Date')
    plt.ylabel('Spread')
    plt.legend()

    # Plot Z-score
    plt.figure(figsize = (8, 5))
    plt.plot(z_score, label = 'Z-score')
    plt.title('Z-score')
    plt.xlabel('Date')
    plt.ylabel('Z-score')
    plt.axhline(1.0, color='r', linestyle='--')
    plt.axhline(-1.0, color='r', linestyle='--')
    plt.axhline(0.0, color='k', linestyle='-')
    plt.legend()
    
    return plt.show()
