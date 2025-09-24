"""Authorities model for user roles"""

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base


class Authorities(Base):
    __tablename__ = "authorities"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String, ForeignKey("accounts.username"), nullable=False)
    role_id = Column(String, ForeignKey("roles.id"), nullable=False)
    
    # Relationships
    account = relationship("Account", back_populates="authorities")
    role = relationship("Role", back_populates="authorities")