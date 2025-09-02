"""Categorization module for applying rules to transactions."""

import re
from typing import Any


def apply_rules(merchant: str, rules_list: list[dict[str, Any]]) -> str:
    """
    Apply the first matching category rule to a merchant string.

    Rules are sorted by priority (higher priority first).
    Patterns are case-insensitive regex.
    If no match, return 'Miscellaneous'.
    """
    for rule in rules_list:
        if re.search(rule["pattern"], merchant.lower()):
            return str(rule.get("category", "Miscellaneous"))
    return "Miscellaneous"
