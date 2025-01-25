import utils as ut
import pandas as pd
import numpy as np

df = pd.read_csv('../data/EURUSD60.csv',
                 names=['Date', 'Open', 'High', 'Low', 'Close', 'Volume'],
                 parse_dates=['Date'], delimiter="\t")

df.set_index('Date', inplace=True)

initial_capital = 10000.0
risk_percentage = 0.03
leverage = 100
shift = -1

df['MA'] = ut.calculate_moving_average(df['Close'], window=12).shift(shift)
df['STDDEV'] = ut.calculate_standard_deviation(
    df['Close'], window=12).shift(shift)
df['UPPER_BAND'] = df['MA'] + (2 * df['STDDEV'])
df['LOWER_BAND'] = df['MA'] - (2 * df['STDDEV'])

df['RSI'] = ut.calculate_rsi(df['Close'], periods=8).shift(shift)

df['BUYS'] = (df['Close'] < df['LOWER_BAND']) & (df['RSI'] < 25)
df['SELLS'] = (df['Close'] > df['UPPER_BAND']) & (df['RSI'] > 75)

df['Position'] = 0
stop_loss_pct = 0.0005
take_profit_pct = 0.001

df['Hour'] = df.index.hour
df['is_trading_hour'] = (df['Hour'] >= 8) & (df['Hour'] <= 16)

current_position = 0
entry_price = 0
stop_loss = 0
take_profit = 0

for i in range(1, len(df)):
    curr_close = df['Close'].iloc[i]
    is_trading_hour = df['is_trading_hour'].iloc[i]

    if current_position == 0 and is_trading_hour:
        if df['BUYS'].iloc[i]:
            current_position = 1
            entry_price = curr_close
            stop_loss = entry_price * (1 - stop_loss_pct)
            take_profit = entry_price * (1 + take_profit_pct)
        elif df['SELLS'].iloc[i]:
            current_position = -1
            entry_price = curr_close
            stop_loss = entry_price * (1 + stop_loss_pct)
            take_profit = entry_price * (1 - take_profit_pct)

    elif current_position != 0:
        if (current_position == 1 and
                (curr_close <= stop_loss or curr_close >= take_profit)):
            current_position = 0
            entry_price = 0
        elif (current_position == -1 and
              (curr_close >= stop_loss or curr_close <= take_profit)):
            current_position = 0
            entry_price = 0

    df.loc[df.index[i], 'Position'] = current_position

df['Returns'] = df['Close'].pct_change()
df['Current_Balance'] = initial_capital
df['Trade_PnL'] = 0.0

for i in range(1, len(df)):
    current_balance = df['Current_Balance'].iloc[i-1]
    current_position_size = current_balance * risk_percentage * leverage

    returns = df['Returns'].iloc[i]
    position = df['Position'].iloc[i-1]
    trade_pnl = position * current_position_size * returns

    df.loc[df.index[i], 'Trade_PnL'] = trade_pnl
    df.loc[df.index[i], 'Current_Balance'] = current_balance + trade_pnl

hourly_pnl_series = df['Trade_PnL'].dropna()
avg_hourly_pnl = hourly_pnl_series.mean()
std_hourly_pnl = hourly_pnl_series.std()

print(f"Strategy Statistics (with {leverage}x leverage):")
print(f"Initial Capital: ${initial_capital:,.2f}")
print(f"Risk per trade: ${initial_capital * risk_percentage:,.2f} ({risk_percentage*100}%)")
print(f"Leverage position size: ${initial_capital * risk_percentage * leverage:,.2f}")
print(f"Average hourly PnL: ${avg_hourly_pnl:.2f}")
print(f"Std hourly PnL: ${std_hourly_pnl:.2f}")

if std_hourly_pnl > 0:
    sharpe_ratio = avg_hourly_pnl/std_hourly_pnl
    annualized_sharpe_ratio = sharpe_ratio * np.sqrt(252 * 24)
    print(f'Hourly Sharpe Ratio: {sharpe_ratio:.4f}')
    print(f'Annualized Sharpe Ratio: {annualized_sharpe_ratio:.4f}')

df['Peak'] = df['Current_Balance'].cummax()
df['Drawdown'] = (df['Current_Balance'] - df['Peak']) / df['Peak']
max_drawdown = df['Drawdown'].min()
print(f'Maximum Drawdown: {max_drawdown:.2%}')
print(f'Final Capital: ${df["Current_Balance"].iloc[-1]:,.2f}')

total_trades = (df['Position'].diff() != 0).sum()
winning_trades = (df['Trade_PnL'] > 0).sum()
print(f'\nTrading Summary:')
print(f'Total Trades: {total_trades}')
print(f'Win Rate: {(winning_trades/total_trades*100):.2f}%')
print(f'Average Trade Duration (hours): {len(df)/total_trades:.1f}')

total_return = (df["Current_Balance"].iloc[-1] -
                initial_capital) / initial_capital * 100
print(f'Total Return: {total_return:.2f}%')
