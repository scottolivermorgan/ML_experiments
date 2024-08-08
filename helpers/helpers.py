import yfinance as yf
import pandas as pd


def get_stock_price(
    ticker: str, start: str = None, end: str = None, interval: str = "1d"
) -> pd.DataFrame:
    """
    Fetches historical stock price data for the given ticker from Yahoo Finance.

    Parameters:
    ticker (str): The stock ticker symbol (e.g., 'AAPL' for Apple Inc.).
    start (str): The start date for fetching data (format: 'YYYY-MM-DD').
                 If None, defaults to the first available date.
    end (str): The end date for fetching data (format: 'YYYY-MM-DD').
               If None, fetches data up to the most recent available date.
    interval (str): The data interval (default is '1d').
                    Valid intervals are '1m', '2m', '5m', '15m', '30m', '60m', '90m', '1h', '1d', '5d', '1wk', '1mo', and '3mo'.

    Returns:
    pd.DataFrame: A DataFrame containing the stock price data.
    """
    try:
        if start is None:
            df = yf.download(ticker, period="max", interval=interval)

        else:
            df = yf.download(ticker, start=start, end=end, interval=interval)
        return df

    except Exception as e:
        print(f"Failed to retrive data for {ticker} with exception {e}")
        return pd.DataFrame()
