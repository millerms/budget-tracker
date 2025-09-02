"""
Streamlit page for adding transactions manually.
"""

from datetime import date
from decimal import Decimal
from typing import cast

import streamlit as st

from ..categorize import apply_rules
from ..db import create_transaction, get_category_rules, get_default_rules
from ..schemas import TransactionCreate


def main() -> None:
    st.title("Add Transaction")

    with st.form("add_txn"):
        date_input = st.date_input("Date", value=date.today())
        merchant_input = st.text_input("Merchant")
        amount_input = st.number_input(
            "Amount",
            step=0.01,
            help="Positive for income, negative for expense",
        )
        account_input = st.selectbox("Account", ["checking", "savings", "credit_card"])
        category_input = st.text_input("Category (auto-assigned if blank)", "")
        submitted = st.form_submit_button("Add Transaction")

    if submitted:
        if not merchant_input or not amount_input or not account_input:
            st.error("Please fill in all required fields.")
        else:
            # Apply category rules if not provided
            if not category_input:
                db_rules = get_category_rules()
                default_rules = get_default_rules()
                all_rules = db_rules + default_rules
                category_input = apply_rules(merchant_input, all_rules)
            else:
                category_input = category_input.strip()

            # Create schema and save
            txn_data = TransactionCreate(
                date=cast(date, date_input),
                merchant=merchant_input,
                amount=Decimal(str(amount_input)),
                account=account_input,
                category=category_input,
                description="",
            )

            result = create_transaction(txn_data)
            st.success(
                f"Transaction added! ID: {result['id']}, Category: {result['category']}"
            )


# Run main
if __name__ == "__main__":
    main()
