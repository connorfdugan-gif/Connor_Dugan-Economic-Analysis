"""
Project configuration for a reusable FRED dashboard.

THIS IS THE MAIN FILE YOU CUSTOMIZE.

Beginner note:
Most project changes should happen here, not in app.py.

Search for the words FILL IN below and replace the placeholder text.
"""

# -----------------------------------------------------------------------------
# PROJECT IDENTITY
# -----------------------------------------------------------------------------
# These values control the title and the top text in the dashboard.

PROJECT_TITLE = "FILL IN: Your Dashboard Title"
PROJECT_SUBTITLE = "FILL IN: One sentence describing your topic"
PROJECT_TAGLINE = "FILL IN: A short polished tagline for your project"

# Main research question shown near the top of the dashboard
RESEARCH_QUESTION = """
FILL IN:
Write 1 to 3 sentences explaining your research question.
Example:
How has inflation changed over time, and how is it related to unemployment,
interest rates, and recession periods?
"""

EXECUTIVE_SUMMARY = (
    "FILL IN: Write a short summary of what your dashboard studies. "
    "This should sound polished and professional."
)

DATASET_DESCRIPTION = (
    "FILL IN: Explain what your selected FRED series represent and why you chose them."
)

# -----------------------------------------------------------------------------
# SERIES SETUP
# -----------------------------------------------------------------------------
# VERY IMPORTANT:
# - The LEFT side must be real FRED series IDs
# - The RIGHT side is the nice label shown in charts and tables
#
# Replace the example series below with your own topic.

SERIES = {
    "FILL_IN_SERIES_ID_1": "FILL IN: Nice label for your main target series",
    "FILL_IN_SERIES_ID_2": "FILL IN: Nice label for supporting variable 1",
    "FILL_IN_SERIES_ID_3": "FILL IN: Nice label for supporting variable 2",
    "FILL_IN_SERIES_ID_4": "FILL IN: Nice label for supporting variable 3",
}

# Optional recession indicator used for gray shaded regions on charts
RECESSION_SERIES_ID = "USREC"
RECESSION_SERIES_LABEL = "U.S. Recession Indicator"

# Start date for pulling data from FRED
# Change this if your series starts later and you want to avoid many missing values
START_DATE = "FILL IN: YYYY-MM-DD"

# Choose the final dashboard frequency
# Use:
# "A" for annual
# "Q" for quarterly
# "M" for monthly
TARGET_FREQUENCY = "FILL IN: A, Q, or M"

# If True, app.py will show debug tables for missing values and column names
# Set this to False before final presentation
SHOW_DEBUG_TABLES = False

# If True, the main chart will draw a horizontal zero line
# This is useful for variables like deficits, growth rates, or net change
ADD_ZERO_LINE_TO_MAIN_CHART = True

# -----------------------------------------------------------------------------
# METRIC CARDS
# -----------------------------------------------------------------------------
# These labels control the 4 metric cards at the top of the dashboard.

PRIMARY_METRIC_LABEL = "FILL IN: Label for latest value"
SECONDARY_METRIC_LABEL = "FILL IN: Label for average value"
LOW_METRIC_LABEL = "FILL IN: Label for minimum"
HIGH_METRIC_LABEL = "FILL IN: Label for maximum"

# -----------------------------------------------------------------------------
# ANALYSIS TARGET AND MODEL FEATURES
# -----------------------------------------------------------------------------
# TARGET_VARIABLE must match one of the keys inside SERIES.
# MODEL_FEATURES should be a list of supporting variables that help explain the target.

TARGET_VARIABLE = "FILL_IN_SERIES_ID_1"

MODEL_FEATURES = [
    "FILL_IN_SERIES_ID_2",
    "FILL_IN_SERIES_ID_3",
    "FILL_IN_SERIES_ID_4",
]

# -----------------------------------------------------------------------------
# OPTIONAL SETTINGS
# -----------------------------------------------------------------------------

TEST_SIZE = 0.2
RANDOM_STATE = 42

# -----------------------------------------------------------------------------
# NARRATIVE TEXT BLOCKS
# -----------------------------------------------------------------------------
# These appear in the dashboard as polished explanation text.

INTRO_PARAGRAPH = (
    "FILL IN: Write a beginner-friendly introduction to the topic and why it matters."
)

METHODS_PARAGRAPH = (
    "FILL IN: Explain how the dashboard collects FRED data, aligns time series, "
    "visualizes trends, and uses a baseline linear regression model."
)

FINDINGS_PARAGRAPH = (
    "FILL IN: Replace this with your final findings after analysis."
)

TEAM_NOTES = (
    "FILL IN: Add a short demo-day note about what the audience should notice."
)

# -----------------------------------------------------------------------------
# SECTION TITLES
# -----------------------------------------------------------------------------

SECTION_TITLES = {
    "overview": "Project Overview",
    "main_chart": "Main Time Series",
    "comparison_groups": "Comparative Views",
    "correlation": "Correlation Analysis",
    "scatter": "Scatterplot Explorer",
    "modeling": "Baseline Modeling",
    "conclusion": "Key Takeaways",
}

# -----------------------------------------------------------------------------
# CHART GROUPS
# -----------------------------------------------------------------------------
# This is how you control the extra comparison charts without editing app.py.
#
# Each group has:
# - title: section title in the dashboard
# - description: explanation below the chart
# - chart_type: keep "line" for now
# - series_ids: list of FRED IDs from SERIES that should appear in that chart

CHART_GROUPS = {
    "group_1": {
        "title": "FILL IN: Comparison chart 1 title",
        "description": (
            "FILL IN: Explain what this chart compares and why it matters."
        ),
        "chart_type": "line",
        "series_ids": ["FILL_IN_SERIES_ID_2", "FILL_IN_SERIES_ID_3"],
    },
    "group_2": {
        "title": "FILL IN: Comparison chart 2 title",
        "description": (
            "FILL IN: Explain what this second comparison chart shows."
        ),
        "chart_type": "line",
        "series_ids": ["FILL_IN_SERIES_ID_4"],
    },
}

# -----------------------------------------------------------------------------
# SERIES DESCRIPTIONS
# -----------------------------------------------------------------------------
# Helpful for documentation, your README, or future expanders/tooltips.

SERIES_DESCRIPTIONS = {
    "FILL_IN_SERIES_ID_1": "FILL IN: Description of target series",
    "FILL_IN_SERIES_ID_2": "FILL IN: Description of supporting series 1",
    "FILL_IN_SERIES_ID_3": "FILL IN: Description of supporting series 2",
    "FILL_IN_SERIES_ID_4": "FILL IN: Description of supporting series 3",
    "USREC": "U.S. recession indicator used for chart shading.",
}
