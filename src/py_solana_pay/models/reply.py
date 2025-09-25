"""Reply model"""

from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from ..database import Base


class Reply(Base):
    __tablename__ = "replies"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    description = Column(String, nullable=False)
    create_date = Column(DateTime, default=datetime.utcnow)
    username = Column(String, ForeignKey("accounts.username"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    comment_id = Column(Integer, ForeignKey("comments.id"), nullable=False)

    # Relationships
    account = relationship("Account", back_populates="replies")
    product = relationship("Product", back_populates="replies")
    comment = relationship("Comment", back_populates="replies")
