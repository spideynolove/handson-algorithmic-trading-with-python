import pandas as pd
import commons as cm

df = pd.read_csv('../data/EURUSD1440.csv',
                 names=['Date', 'Open', 'High', 'Low', 'Close', 'Volume'],
                 parse_dates=['Date'], delimiter="\t")

df.set_index('Date', inplace=True)

initial_capital = 10000.0
risk_percentage = 0.03
leverage = 100
shift = -2

base_risk_amount = initial_capital * risk_percentage
position_size = base_risk_amount * leverage

df['MA'] = cm.calculate_moving_average(df['Close'], window=20).shift(shift)
df['STDDEV'] = cm.calculate_standard_deviation(
    df['Close'], window=20).shift(shift)
df['UPPER_BAND'] = df['MA'] + (2 * df['STDDEV'])
df['LOWER_BAND'] = df['MA'] - (2 * df['STDDEV'])

df['RSI'] = cm.calculate_rsi(df['Close']).shift(shift)

df['BUYS'] = (df['Close'] < df['LOWER_BAND']) & (df['RSI'] < 30)
df['SELLS'] = (df['Close'] > df['UPPER_BAND']) & (df['RSI'] > 70)

df['Position'] = 0
stop_loss_pct = 0.001
take_profit_pct = 0.002

current_position = 0
entry_price = 0
stop_loss = 0
take_profit = 0

for i in range(1, len(df)):
    prev_close = df['Close'].iloc[i-1]
    curr_close = df['Close'].iloc[i]

    if current_position == 0:
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

    elif current_position == 1:
        if curr_close <= stop_loss or curr_close >= take_profit:
            current_position = 0
            entry_price = 0
    elif current_position == -1:
        if curr_close >= stop_loss or curr_close <= take_profit:
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

daily_pnl_series = df['Trade_PnL'].dropna()
avg_daily_pnl = daily_pnl_series.mean()
std_daily_pnl = daily_pnl_series.std()

print(f"Strategy Statistics (with {leverage}x leverage):")
print(f"Initial Capital: ${initial_capital:,.2f}")
print(f"Risk per trade: ${base_risk_amount:,.2f} ({risk_percentage*100}%)")
print(f"Position size: ${position_size:,.2f} ({leverage}x leverage)")
print(f"Average daily PnL: ${avg_daily_pnl:.2f}")
print(f"Std daily PnL: ${std_daily_pnl:.2f}")

if std_daily_pnl > 0:
    sharpe_ratio = cm.calculate_sharpe_ratio(daily_pnl_series)
    annualized_sharpe_ratio = cm.calculate_annualized_sharpe_ratio(
        sharpe_ratio)
    print(f'Sharpe Ratio: {sharpe_ratio:.4f}')
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

total_return = (df["Current_Balance"].iloc[-1] -
                initial_capital) / initial_capital * 100
print(f'Total Return: {total_return:.2f}%')
