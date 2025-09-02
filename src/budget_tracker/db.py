"""
Database connection and SQLAlchemy metadata setup.
Creates tables on import for MVP.
"""

from sqlalchemy import create_engine, MetaData

from .config import config

engine = create_engine(config.database_url, echo=config.app_env == "dev")

meta = MetaData()

metadata = meta
