"""
Data loading utilities for the FRED dashboard.

This file handles:
- loading your FRED API key
- fetching one series at a time
- merging multiple series together
- resampling everything to one common frequency

Beginner note:
If your charts look blank or you see lots of missing values,
this is one of the first files to check.
"""

import os
import pandas as pd
from fredapi import Fred
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Read the FRED API key
FRED_API_KEY = os.getenv("FRED_API_KEY")

if not FRED_API_KEY:
    raise ValueError(
        "Missing FRED_API_KEY. Create a .env file in the project root."
    )

# Create the FRED client one time
fred = Fred(api_key=FRED_API_KEY)


def fetch_series(series_id: str, start_date: str) -> pd.DataFrame:
    """
    Fetch one FRED series and return a dataframe with:
    - date
    - one value column named exactly like the series ID

    Example output columns:
    - date
    - UNRATE
    """
    series = fred.get_series(series_id, observation_start=start_date)

    df = series.reset_index()
    df.columns = ["date", series_id]
    df["date"] = pd.to_datetime(df["date"])

    return df


def resample_to_target_frequency(df: pd.DataFrame, target_frequency: str) -> pd.DataFrame:
    """
    Convert mixed-frequency data into one final frequency.

    Use:
    - "A" for annual
    - "Q" for quarterly
    - "M" for monthly

    Why this matters:
    Some FRED series are annual, some monthly, some quarterly.
    If you merge them without resampling, charts can look broken.
    """
    df = df.copy().set_index("date")

    if target_frequency == "A":
        # Use the last available value in each year
        df = df.resample("YE").last()
    elif target_frequency == "Q":
        # Use the last available value in each quarter
        df = df.resample("QE").last()
    elif target_frequency == "M":
        # Use the last available value in each month
        df = df.resample("ME").last()
    else:
        raise ValueError("Unsupported TARGET_FREQUENCY. Use 'A', 'Q', or 'M'.")

    # Fill forward after resampling so chart lines are more complete
    df = df.ffill()

    # Recession data should be 0 or 1
    if "USREC" in df.columns:
        df["USREC"] = (df["USREC"] > 0).astype(int)

    return df.reset_index()


def load_fred_data(main_series: dict, supporting_series: list, start_date: str, target_frequency: str) -> pd.DataFrame:
    """
    Load the main series plus supporting series, merge them by date,
    then resample everything to the frequency chosen in config.py.

    Parameters
    ----------
    main_series : dict
        Example:
        {"id": "UNRATE", "label": "Unemployment Rate"}

    supporting_series : list
        Example:
        [{"id": "CPIAUCSL", "label": "Consumer Price Index"}]

    start_date : str
        Example:
        "1990-01-01"

    target_frequency : str
        One of "A", "Q", or "M"
    """
    # Start with the target series
    df = fetch_series(main_series["id"], start_date=start_date)

    # Merge each supporting series onto the same dataframe
    for series in supporting_series:
        temp = fetch_series(series["id"], start_date=start_date)
        df = df.merge(temp, on="date", how="outer")

    # Sort before resampling
    df = df.sort_values("date").reset_index(drop=True)

    # Align all series to a common frequency
    df = resample_to_target_frequency(df, target_frequency=target_frequency)

    return df
