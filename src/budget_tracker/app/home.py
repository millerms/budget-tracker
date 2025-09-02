"""Minimal Streamlit home page for Budget Tracker.

Provides a simple entry point and a button to open the
Add Transaction flow within the same process.
"""

import streamlit as st


def main() -> None:
    """Render the home page UI."""
    st.set_page_config(page_title="Budget Tracker", page_icon="💰")
    st.title("Budget Tracker")
    st.write(
        "Welcome! Use the button below to add a transaction. "
        "The FastAPI service should be running separately on port 8000."
    )

    if st.button("Add a Transaction"):
        # Local import to avoid Streamlit re-run import cycles
        from .add_transaction import main as add_txn_main

        add_txn_main()


if __name__ == "__main__":
    main()
