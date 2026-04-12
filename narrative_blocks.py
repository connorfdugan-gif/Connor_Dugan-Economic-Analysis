"""
Optional reusable narrative text helpers.

Beginner note:
You do NOT have to use this file in app.py right away.
It is here in case you want easy text generators for future versions.
"""

def project_hook(question: str) -> str:
    """
    Build a short opening sentence based on the research question.
    """
    return (
        f"This dashboard is built around the question: {question} "
        "It is designed to show that a polished data product can still remain flexible, "
        "interpretable, and easy to customize."
    )


def data_context_paragraph(series_labels: dict) -> str:
    """
    Turn a dictionary of series labels into a paragraph.
    """
    pretty = ", ".join([f"{sid} ({label})" for sid, label in series_labels.items()])
    return (
        "The selected indicators were chosen to represent the main concepts in the research question. "
        f"In this version, the dashboard includes {pretty}. "
        "Because the structure is config-driven, the same workflow can be reused for different economic themes."
    )


def modeling_paragraph() -> str:
    """
    Return a short explanation of the modeling section.
    """
    return (
        "The modeling section is intentionally lightweight. "
        "It is included as a baseline analytical extension rather than a claim of causal inference. "
        "For a presentation, this helps demonstrate feature selection, model evaluation, "
        "and interpretability without overcomplicating the project."
    )


def presentation_tip() -> str:
    """
    Return a short tip for how to demo the dashboard live.
    """
    return (
        "For demo day, guide viewers through the narrative in order: "
        "the question, the chosen variables, what changed over time, "
        "what correlations appear, and what the model can and cannot tell us."
    )
