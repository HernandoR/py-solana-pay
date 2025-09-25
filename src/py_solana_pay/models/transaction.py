"""Transaction model"""

from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from ..database import Base


class Transaction(Base):
    __tablename__ = "transactions"

    transaction_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    transaction_type = Column(String)
    transaction_date = Column(DateTime, default=datetime.utcnow)
    transaction_details = Column(String)
    username = Column(String, ForeignKey("accounts.username"), nullable=False)

    # Relationships
    account = relationship("Account", back_populates="transactions")
