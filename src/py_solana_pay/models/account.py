"""Account model"""

from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from ..database import Base


class Account(Base):
    __tablename__ = "accounts"
    
    username = Column(String, primary_key=True, index=True)
    password = Column(String, nullable=False)
    email = Column(String, unique=True, index=True)
    fullname = Column(String)
    photo = Column(String)
    wallet_key = Column(String)  # Solana wallet public key
    
    # Relationships (back_populates will be set in the related models)
    authorities = relationship("Authorities", back_populates="account")
    bank_accounts = relationship("BankAccount", back_populates="account")
    transactions = relationship("Transaction", back_populates="account")
    comments = relationship("Comment", back_populates="account")
    replies = relationship("Reply", back_populates="account")