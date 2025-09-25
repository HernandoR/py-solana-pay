"""Role model"""

from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from ..database import Base


class Role(Base):
    __tablename__ = "roles"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)

    # Relationships
    authorities = relationship("Authorities", back_populates="role")
