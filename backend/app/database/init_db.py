"""
=========================================================
JARVIS Database Initialization
=========================================================
"""

from app.database.base import Base
from app.database.models import User
from app.database.session import engine


def init_database() -> None:
    """
    Create all database tables.
    """

    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    init_database()
    print("Database initialized successfully!")