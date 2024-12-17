import pandas as pd
import matplotlib.pyplot as plt
import commons as cm

CHART_SIZE = (18, 12)

spx_prices = pd.read_csv('../data/spx.csv', index_col=0, parse_dates=True)

spx_prices.plot(figsize=(CHART_SIZE), color='black')

spx_prices.loc['2008'].plot(figsize=(CHART_SIZE), color='black')

spx_prices['SPX_MA'] = cm.calculate_moving_average(spx_prices['SPX'], window=40)
spx_prices.bfill(inplace=True)

spx_prices['SPX'].plot(figsize=(CHART_SIZE), linestyle='--', color='black', legend='SPX')
spx_prices['SPX_MA'].plot(figsize=(CHART_SIZE), linestyle='-', color='grey', legend='SPX_MA')

spx_prices['SPX']['2008'].plot(figsize=(CHART_SIZE), linestyle='--', color='black', legend='SPX')
spx_prices['SPX_MA']['2008'].plot(figsize=(CHART_SIZE), linestyle='-', color='grey', legend='SPX_MA')

spx_prices['SPX_STDDEV'] = cm.calculate_standard_deviation(spx_prices['SPX'], window=40)

spx_prices.bfill(inplace=True)

spx_prices['SPX_STDDEV'].plot(figsize=(CHART_SIZE), linestyle='-', color='black', legend='SPX_STDDEV')

spx_prices['SPX_UPPER_BAND'] = spx_prices['SPX_MA'] + 2 * spx_prices['SPX_STDDEV']
spx_prices['SPX_LOWER_BAND'] = spx_prices['SPX_MA'] - 2 * spx_prices['SPX_STDDEV']

spx_prices['SPX'].plot(figsize=(CHART_SIZE), linestyle='--', color='grey', legend='SPX')
spx_prices['SPX_MA'].plot(figsize=(CHART_SIZE), linestyle='-', color='grey', legend='SPX_MA')
spx_prices['SPX_UPPER_BAND'].plot(figsize=(CHART_SIZE), linestyle=':', color='black', legend='SPX_UPPER_BAND')
spx_prices['SPX_LOWER_BAND'].plot(figsize=(CHART_SIZE), linestyle='-.', color='black', legend='SPX_LOWER_BAND')

spx_prices['SPX']['2008'].plot(figsize=(CHART_SIZE), linestyle='--', color='grey', legend='SPX')
spx_prices['SPX_MA']['2008'].plot(figsize=(CHART_SIZE), linestyle='-', color='grey', legend='SPX_MA')
spx_prices['SPX_UPPER_BAND']['2008'].plot(figsize=(CHART_SIZE), linestyle=':', color='black', legend='SPX_UPPER_BAND')
spx_prices['SPX_LOWER_BAND']['2008'].plot(figsize=(CHART_SIZE), linestyle='-.', color='black', legend='SPX_LOWER_BAND')

spx_prices['BUYS'] = spx_prices['SPX'] < spx_prices['SPX_LOWER_BAND']
spx_prices['SELLS'] = spx_prices['SPX'] > spx_prices['SPX_UPPER_BAND']

spx_prices[['SPX', 'SPX_UPPER_BAND', 'SPX_LOWER_BAND', 'BUYS', 'SELLS']][(spx_prices['BUYS'] | spx_prices['SELLS'])]

fig = plt.figure()
ax = fig.add_subplot(111)

spx_prices_2007_2009 = spx_prices['2007':'2009']
spx_prices_2007_2009['SPX'].plot(ax=ax, figsize=(CHART_SIZE), linestyle='--', color='grey', legend='SPX')
spx_prices_2007_2009['SPX_UPPER_BAND'].plot(ax=ax, figsize=(CHART_SIZE), linestyle=':', color='black', legend='SPX_UPPER_BAND')
spx_prices_2007_2009['SPX_LOWER_BAND'].plot(ax=ax, figsize=(CHART_SIZE), linestyle='-.', color='black', legend='SPX_LOWER_BAND')
ax.plot(spx_prices_2007_2009.loc[spx_prices_2007_2009['BUYS']].index, spx_prices_2007_2009['SPX'][spx_prices_2007_2009['BUYS']], '^', color='black', markersize=15, alpha=0.5)
ax.plot(spx_prices_2007_2009.loc[spx_prices_2007_2009['SELLS']].index, spx_prices_2007_2009['SPX'][spx_prices_2007_2009['SELLS']], 'v', color='black', markersize=15, alpha=0.5)
plt.show()
