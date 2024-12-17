import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import commons as cm

dates = pd.date_range('1992-01-01', '2012-10-22')

np.random.seed(1)

pnls = np.random.randint(-990, 1000, size=len(dates))
pnls = pnls.cumsum()

positions = np.random.randint(-1, 2, size=len(dates))
positions = positions.cumsum()

strategy_performance = pd.DataFrame(
    index=dates, data={'PnL': pnls, 'Position': positions})
strategy_performance['PnL'].plot(figsize=(18, 12), color='black', legend='PnL')

strategy_performance['PnLStdev'] = cm.calculate_standard_deviation(
    strategy_performance['PnL'], window=20).bfill()
strategy_performance['PnLStdev'].plot(
    figsize=(18, 12), color='black', legend='PnLStdev')

daily_pnl_series = strategy_performance['PnL'].shift(
    -1) - strategy_performance['PnL']
daily_pnl_series.fillna(0, inplace=True)
avg_daily_pnl = daily_pnl_series.mean()
std_daily_pnl = daily_pnl_series.std()
sharpe_ratio = cm.calculate_sharpe_ratio(daily_pnl_series)
annualized_sharpe_ratio = cm.calculate_annualized_sharpe_ratio(sharpe_ratio)

strategy_performance['PnL'].plot(figsize=(12, 6), color='black', legend='PnL')
plt.axhline(y=28000, color='darkgrey', linestyle='--',
            label='PeakPnLBeforeDrawdown')
plt.axhline(y=-15000, color='darkgrey', linestyle=':',
            label='TroughPnLAfterDrawdown')
plt.vlines(x='2000', ymin=-15000, ymax=28000,
           label='MaxDrawdown', color='black', linestyle='-.')
plt.legend()
plt.show()
