from zipline.api import order, record, symbol
from zipline.finance import commission, slippage
from zipline import run_algorithm
import pandas as pd
import pandas_datareader.data as web
import matplotlib.pyplot as plt


def initialize(context):
    context.asset = symbol("AAPL")
    context.set_commission(commission.PerShare(
        cost=0.0075, min_trade_cost=1.0))
    context.set_slippage(slippage.VolumeShareSlippage())


def handle_data(context, data):
    order(context.asset, 10)
    record(AAPL=data.current(context.asset, "price"))


def analyze(context=None, results=None):
    import matplotlib.pyplot as plt

    ax1 = plt.subplot(211)
    results.portfolio_value.plot(ax=ax1)
    ax1.set_ylabel("Portfolio value (USD)")
    ax2 = plt.subplot(212, sharex=ax1)
    results.AAPL.plot(ax=ax2)
    ax2.set_ylabel("AAPL price (USD)")

    plt.gcf().set_size_inches(18, 8)
    plt.show()


start = pd.Timestamp("2014")
end = pd.Timestamp("2018")

sp500 = web.DataReader("SP500", "fred", start, end).SP500
benchmark_returns = sp500.pct_change()
print(benchmark_returns.head())

result = run_algorithm(
    start=start,
    end=end,
    initialize=initialize,
    handle_data=handle_data,
    capital_base=100000,
    benchmark_returns=benchmark_returns,
    bundle="quandl",
    data_frequency="daily",
)

print(result.info())

result.portfolio_value.plot()
plt.show()
