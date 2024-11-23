import yfinance as yf
import pandas as pd
import os
from pathlib import Path


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


def rename_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Renames all columns in the DataFrame to uppercase and replaces spaces with underscores.

    Parameters:
    df (pd.DataFrame): The input DataFrame.

    Returns:
    pd.DataFrame: The DataFrame with renamed columns.
    """
    df.columns = df.columns.str.upper().str.replace(' ', '_')
    return df


def clean_stock_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans and processes the stock data DataFrame.

    Parameters:
    df (pd.DataFrame): The input DataFrame containing stock price data.

    Returns:
    pd.DataFrame: The cleaned and processed DataFrame.
    """
    # Ensure the index is of datetime type
    df.index = pd.to_datetime(df.index)

    # Ensure the expected columns are all floats
    expected_float_columns = ['OPEN', 'HIGH', 'LOW', 'CLOSE', 'ADJ_CLOSE', 'VOLUME']
    df[expected_float_columns] = df[expected_float_columns].astype(float)

    # Order the DataFrame by index from oldest to newest
    df = df.sort_index(ascending=True)

    # Forward fill followed by backward fill to handle NaN values
    df = df.ffill().bfill()

    return df


def create_output_folders():
    # Define the folder paths
    folders = ['outputs/data', 'outputs/plots']

    for folder in folders:
        # Use pathlib to create the Path object
        path = Path(folder)

        # Check if the folder exists
        if not path.exists():
            # If not, create the folder
            path.mkdir(parents=True, exist_ok=True)
            print(f"Folder '{folder}' created.")
        else:
            print(f"Folder '{folder}' already exists.")


def load_and_prepare_csv(file_path):
    # Load the CSV file into a DataFrame
    df = pd.read_csv(file_path)
    
    # Convert the 'Date' column to datetime
    df['Date'] = pd.to_datetime(df['Date'])
    
    # Set the 'Date' column as the index
    df.set_index('Date', inplace=True)

    # Sort the DataFrame by the Date index
    df.sort_index(inplace=True)
    
    # Convert all other columns to float
    df = df.astype(float)
    
    return df