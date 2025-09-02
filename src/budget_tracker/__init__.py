"""Budget Tracker package."""

__version__ = "0.1.0"

# Avoid importing settings at package import time to prevent runtime
# dependencies (like pydantic-settings) from being required in tests
# that only need submodules.
__all__ = ["__version__"]
