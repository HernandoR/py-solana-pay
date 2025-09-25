"""Product model"""

from sqlalchemy import Column, Float, Integer, String
from sqlalchemy.orm import relationship

from ..database import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    image = Column(String)
    quantity = Column(Integer, default=0)

    # Relationships
    comments = relationship("Comment", back_populates="product")
    replies = relationship("Reply", back_populates="product")
