"""
=========================================================
JARVIS Base Service
=========================================================

Provides common database transaction helpers
for all service classes.

Author: Abhinay Kumar
Project: JARVIS
=========================================================
"""

from sqlalchemy.orm import Session


class BaseService:
    """
    Base class for all services.
    """

    def __init__(self, db: Session):
        self.db = db

    def commit(self):
        """
        Commit current transaction.
        """
        self.db.commit()

    def rollback(self):
        """
        Roll back current transaction.
        """
        self.db.rollback()

    def refresh(self, instance):
        """
        Refresh an ORM instance.
        """
        self.db.refresh(instance)