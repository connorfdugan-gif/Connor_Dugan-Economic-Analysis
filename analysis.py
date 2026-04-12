"""
Analysis utilities for the FRED dashboard.

This file handles:
- metric card formatting
- summary statistics
- the baseline linear regression model

Beginner note:
This project uses LINEAR REGRESSION, not logistic regression.
Use linear regression when your target variable is numeric.
"""

import pandas as pd
from sklearn.linear_model import LinearRegression


def format_metric(value) -> str:
    """
    Format a number nicely for Streamlit metric cards.

    If the value is missing, show N/A.
    Otherwise show 2 decimal places.
    """
    if pd.isna(value):
        return "N/A"
    return f"{value:.2f}"


def compute_summary_metrics(series: pd.Series) -> dict:
    """
    Compute summary statistics for the target series.

    Returns a dictionary used by the top 4 metric cards in app.py.
    """
    clean = series.dropna()

    if clean.empty:
        return {
            "latest": "N/A",
            "average": "N/A",
            "minimum": "N/A",
            "maximum": "N/A",
        }

    return {
        "latest": format_metric(clean.iloc[-1]),
        "average": format_metric(clean.mean()),
        "minimum": format_metric(clean.min()),
        "maximum": format_metric(clean.max()),
    }


def build_regression_table(df: pd.DataFrame, target_col: str, feature_cols: list):
    """
    Fit a simple linear regression model.

    Parameters
    ----------
    df : pd.DataFrame
        Dataframe containing the target and feature columns

    target_col : str
        Name of the dependent variable

    feature_cols : list
        Names of explanatory variables

    Returns
    -------
    tuple
        (coef_df, r2)
        If not enough data is available, returns (None, None)

    Beginner explanation:
    - X = feature columns
    - y = target column
    - LinearRegression learns how X relates to y
    """
    model_df = df[[target_col] + feature_cols].dropna().copy()

    # Do not fit a model if there is almost no data
    if model_df.empty or len(model_df) < 5:
        return None, None

    X = model_df[feature_cols]
    y = model_df[target_col]

    model = LinearRegression()
    model.fit(X, y)

    coef_df = pd.DataFrame({
        "Feature": feature_cols,
        "Coefficient": model.coef_
    }).sort_values("Coefficient", ascending=False)

    r2 = model.score(X, y)

    return coef_df, r2
