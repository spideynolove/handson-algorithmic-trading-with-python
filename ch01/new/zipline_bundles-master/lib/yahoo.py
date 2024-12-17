import yfinance as yf
import pandas as pd
import datetime as dt

def get_downloader(start_date,
               end_date,
               granularity='daily'):
    """returns a downloader closure for oanda
    :param start_date: the first day on which dat are downloaded
    :param end_date: the last day on which data are downloaded
    :param granularity: the frequency of price data, 'D' for daily and 'M1' for 1-minute data
    :type start_date: str in format YYYY-MM-DD
    :type end_date: str in format YYYY-MM-DD
    :type granularity: str
    """

    def downloader(symbol):
        """downloads symbol price data using oanda REST API
        :param symbol: the symbol name
        :type symbol: str
        """
        # Create Ticker object
        ticker = yf.Ticker(symbol)
        
        # Get historical data
        interval = '1d' if granularity == 'daily' else '1m'
        df = ticker.history(start=start_date, end=end_date, interval=interval)
        
        if df.empty:
            raise ValueError('Fetching price data for "{}" failed.'.format(symbol))
        
        # Rename columns to match original format
        df = df.rename(columns={
            'Open': 'open',
            'Close': 'close',
            'Low': 'low',
            'High': 'high',
            'Volume': 'volume'
        })
        
        # Get dividends and splits
        dividends = ticker.dividends
        splits = ticker.splits
        
        # Add dividend column
        if not dividends.empty:
            df['dividend'] = dividends.reindex(df.index).fillna(0)
        else:
            df['dividend'] = 0
            
        # Add split column
        if not splits.empty:
            df['split'] = splits.reindex(df.index).fillna(1)
        else:
            df['split'] = 1
            
        print(df.head(3))
        
        return df

    return downloader