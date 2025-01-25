import pandas as pd
import numpy as np

def calculate_sharpe_ratio(returns, risk_free_rate=0):
    excess_returns = returns - risk_free_rate
    sharpe_ratio = excess_returns.mean() / excess_returns.std()
    return sharpe_ratio

def calculate_annualized_sharpe_ratio(sharpe_ratio, periods_per_year=252):
    annualized_sharpe_ratio = sharpe_ratio * np.sqrt(periods_per_year)
    return annualized_sharpe_ratio

def calculate_rsi(data, periods=14):
    delta = data.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=periods).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=periods).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

def calculate_bollinger_bands(data, window=20, num_std=2):
    ma = data.rolling(window=window).mean()
    std = data.rolling(window=window).std()
    upper_band = ma + num_std * std
    lower_band = ma - num_std * std
    return ma, upper_band, lower_band

def calculate_moving_average(data, window=20):
    ma = data.rolling(window=window).mean()
    return ma

def calculate_standard_deviation(data, window=20):
    std = data.rolling(window=window).std()
    return std

def calculate_daily_pnl(returns):
    daily_pnl = returns.diff().dropna()
    return daily_pnl

def calculate_trade_pnl(position, returns, position_size):
    trade_pnl = position * position_size * returns
    return trade_pnl

def calculate_max_drawdown(balance):
    peak = balance.cummax()
    drawdown = (balance - peak) / peak
    max_drawdown = drawdown.min()
    return max_drawdown
