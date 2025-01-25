import pandas as pd
import numpy as np
import utils as ut

df = pd.read_csv('../data/EURUSD1440.csv', 
                 names=['Date', 'Open', 'High', 'Low', 'Close', 'Volume'], 
                 parse_dates=['Date'], delimiter="\t")

df.set_index('Date', inplace=True)

initial_capital = 10000
position_size = 100  

df['Returns'] = df['Close'].pct_change()

positions = np.random.randint(-1, 2, size=len(df))
df['Position'] = positions

df['Strategy_Returns'] = df['Position'].shift(1) * df['Returns']
df['Strategy_Returns'] = df['Strategy_Returns'].fillna(0)  
df['Cumulative_Returns'] = df['Strategy_Returns'].cumsum()
df['PnL'] = initial_capital * (1 + df['Cumulative_Returns'])

df['PnLStdev'] = ut.calculate_standard_deviation(df['PnL'], window=20)

print("First few rows of final dataframe:")
print(df[['Position', 'Returns', 'Strategy_Returns', 'PnL']].head())
print("\nDataframe stats:")
print(df[['Position', 'Returns', 'Strategy_Returns', 'PnL']].describe())

daily_pnl_series = df['PnL'].diff().dropna()
avg_daily_pnl = daily_pnl_series.mean()
std_daily_pnl = daily_pnl_series.std()

print(f"\nAverage daily PnL: {avg_daily_pnl:.2f}")
print(f"Std daily PnL: {std_daily_pnl:.2f}")

if std_daily_pnl == 0 or pd.isna(std_daily_pnl):
    print('Error: Standard deviation is zero or NaN')
else:
    sharpe_ratio = ut.calculate_sharpe_ratio(daily_pnl_series)
    annualized_sharpe_ratio = ut.calculate_annualized_sharpe_ratio(sharpe_ratio)
    print('Sharpe Ratio: {:.4f}'.format(sharpe_ratio))
    print('Annualized Sharpe Ratio: {:.4f}'.format(annualized_sharpe_ratio))

df['Peak'] = df['PnL'].cummax()
df['Drawdown'] = (df['PnL'] - df['Peak']) / df['Peak']
max_drawdown = df['Drawdown'].min()
print('Maximum Drawdown: {:.2%}'.format(max_drawdown))

print(f'Final Capital: ${df["PnL"].iloc[-1]:.2f}')
