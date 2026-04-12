"""
Visualization utilities for the FRED dashboard.

This file contains reusable Plotly chart functions so app.py stays cleaner.
"""

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd


def add_recession_shading(fig, df: pd.DataFrame, recession_col: str):
    """
    Add gray shading to charts during recession periods.

    Assumes the recession column contains 0 and 1 values.
    """
    if recession_col not in df.columns:
        return fig

    rec = df[["date", recession_col]].dropna().copy()
    if rec.empty:
        return fig

    in_recession = False
    start_date = None

    for _, row in rec.iterrows():
        if row[recession_col] == 1 and not in_recession:
            in_recession = True
            start_date = row["date"]
        elif row[recession_col] == 0 and in_recession:
            fig.add_vrect(
                x0=start_date,
                x1=row["date"],
                fillcolor="gray",
                opacity=0.15,
                line_width=0
            )
            in_recession = False

    if in_recession:
        fig.add_vrect(
            x0=start_date,
            x1=rec["date"].max(),
            fillcolor="gray",
            opacity=0.15,
            line_width=0
        )

    return fig


def plot_time_series(df: pd.DataFrame, y_col: str, title: str, recession_col=None, add_zero_line=False):
    """
    Plot one variable over time.
    """
    fig = px.line(df, x="date", y=y_col, title=title)

    if add_zero_line:
        fig.add_hline(y=0, line_dash="dash")

    if recession_col:
        fig = add_recession_shading(fig, df, recession_col)

    fig.update_layout(height=500)
    return fig


def plot_multi_line_chart(df: pd.DataFrame, y_cols: list, title: str, recession_col=None):
    """
    Plot multiple series on one chart.
    """
    fig = go.Figure()

    for col in y_cols:
        if col in df.columns:
            fig.add_trace(
                go.Scatter(
                    x=df["date"],
                    y=df[col],
                    mode="lines",
                    name=col
                )
            )

    if recession_col:
        fig = add_recession_shading(fig, df, recession_col)

    fig.update_layout(title=title, height=500)
    return fig


def plot_correlation_heatmap(df: pd.DataFrame, title: str):
    """
    Plot a correlation matrix.
    """
    corr = df.corr(numeric_only=True)

    fig = px.imshow(
        corr,
        text_auto=True,
        aspect="auto",
        title=title
    )
    fig.update_layout(height=500)
    return fig


def plot_scatter_with_trendline(df: pd.DataFrame, x_col: str, y_col: str, title: str):
    """
    Plot a scatterplot with an OLS trendline.
    """
    fig = px.scatter(
        df,
        x=x_col,
        y=y_col,
        trendline="ols",
        title=title
    )
    fig.update_layout(height=500)
    return fig
