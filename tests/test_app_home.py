"""Smoke test for Streamlit home page import."""


def test_home_import() -> None:
    try:
        # If package is installed
        from budget_tracker.app import home  # type: ignore
    except ModuleNotFoundError:
        # Fallback for src layout
        import os
        import sys

        sys.path.insert(0, os.path.abspath("src"))
        from budget_tracker.app import home  # type: ignore

    assert hasattr(home, "main") and callable(home.main)

