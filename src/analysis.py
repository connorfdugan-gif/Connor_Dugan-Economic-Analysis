"""
Analysis utilities for the FRED dashboard.

This file handles:
- metric card formatting
- summary statistics
- the baseline linear regression model with train/test evaluation
"""

import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error, r2_score


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


def build_regression_table(df: pd.DataFrame, target_col: str, feature_cols: list,
                           test_size: float = 0.2, random_state: int = 42):
    """
    Fit a linear regression with a train/test split and return
    standardized coefficients plus evaluation metrics.

    Parameters
    ----------
    df : pd.DataFrame
        Dataframe containing the target and feature columns
    target_col : str
        Name of the dependent variable
    feature_cols : list
        Names of explanatory variables
    test_size : float
        Fraction of data held out for evaluation (default 0.2)
    random_state : int
        Seed for the split so results are reproducible

    Returns
    -------
    tuple
        (coef_df, metrics)
        If not enough data is available, returns (None, None)

    Beginner explanation:
    - We split the data so we can evaluate the model on rows it never saw.
    - We STANDARDIZE features (subtract mean, divide by std) so that
      coefficients from different predictors are directly comparable.
      A standardized coefficient of 1.5 means: a 1 standard deviation
      increase in that feature moves the target by 1.5 units.
    - We report both R² (variance explained) and MAE (average error
      in the target's original units — here, millions of vehicles).
    """
    model_df = df[[target_col] + feature_cols].dropna().copy()

    # Need enough rows to split meaningfully
    if model_df.empty or len(model_df) < 10:
        return None, None

    X = model_df[feature_cols]
    y = model_df[target_col]

    # Random split. Note: for a pure time-series forecasting study,
    # a chronological split is often more honest — but for learning
    # feature importance, random works fine here.
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state
    )

    # Standardize on the training set only, then apply to test set
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # Fit on standardized data → coefficients are comparable
    model = LinearRegression()
    model.fit(X_train_scaled, y_train)

    # Evaluate on held-out test set
    y_pred_test = model.predict(X_test_scaled)
    test_r2 = r2_score(y_test, y_pred_test)
    test_mae = mean_absolute_error(y_test, y_pred_test)
    train_r2 = model.score(X_train_scaled, y_train)

    # Also fit on RAW (unstandardized) data to report raw coefficients
    # for anyone who wants them in the original units
    model_raw = LinearRegression()
    model_raw.fit(X_train, y_train)

    coef_df = pd.DataFrame({
        "Feature": feature_cols,
        "Raw Coefficient": model_raw.coef_,
        "Standardized Coefficient": model.coef_,
    }).sort_values("Standardized Coefficient", key=abs, ascending=False).reset_index(drop=True)

    metrics = {
        "train_r2": train_r2,
        "test_r2": test_r2,
        "test_mae": test_mae,
        "n_train": len(X_train),
        "n_test": len(X_test),
    }

    return coef_df, metrics

def build_regime_comparison(df: pd.DataFrame, target_col: str, feature_cols: list,
                             periods: int = 12, test_size: float = 0.2,
                             random_state: int = 42) -> dict:
    """
    Fit separate regressions on positive vs. negative YoY growth periods.

    Beginner explanation:
    - "Regime" = a period of time with a distinct economic character.
    - We label each month as "positive growth" or "negative growth"
      based on whether vehicle sales are higher than they were 12 months ago.
    - We then fit a separate model on each regime.
    - If the standardized coefficients rank features differently in the two
      regimes, that's evidence the relationship is regime-dependent —
      which is what the executive summary claims.

    Parameters
    ----------
    periods : int
        Lookback window for YoY growth. Default 12 (for monthly data).
        Use 4 for quarterly, 1 for annual.
    """
    work_df = df[[target_col] + feature_cols].dropna().copy()
    work_df = work_df.reset_index(drop=True)

    if len(work_df) < periods + 10:
        return {
            "positive": {"coef_df": None, "metrics": None, "n_obs": 0},
            "negative": {"coef_df": None, "metrics": None, "n_obs": 0},
        }

    # YoY growth of the target variable
    work_df["_yoy"] = work_df[target_col].pct_change(periods=periods)
    work_df = work_df.dropna(subset=["_yoy"])

    positive_df = work_df[work_df["_yoy"] > 0].copy()
    negative_df = work_df[work_df["_yoy"] <= 0].copy()

    pos_coef, pos_metrics = build_regression_table(
        positive_df, target_col, feature_cols,
        test_size=test_size, random_state=random_state,
    )
    neg_coef, neg_metrics = build_regression_table(
        negative_df, target_col, feature_cols,
        test_size=test_size, random_state=random_state,
    )

    return {
        "positive": {
            "coef_df": pos_coef,
            "metrics": pos_metrics,
            "n_obs": len(positive_df),
        },
        "negative": {
            "coef_df": neg_coef,
            "metrics": neg_metrics,
            "n_obs": len(negative_df),
        },
    }