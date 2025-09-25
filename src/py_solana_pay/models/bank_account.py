"""Bank Account model"""

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from ..database import Base


class BankAccount(Base):
    __tablename__ = "bank_accounts"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    account_number = Column(String, nullable=False)
    bank_name = Column(String)
    account_holder_name = Column(String)
    username = Column(String, ForeignKey("accounts.username"), nullable=False)

    # Relationships
    account = relationship("Account", back_populates="bank_accounts")
