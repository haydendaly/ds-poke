from enum import Enum

from sqlalchemy import Column, DateTime, Enum, Float, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .base import Base
from .enums.market import Market


class Seller(Base):
    __tablename__ = "seller"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    rating = Column(Float, nullable=False)
    location = Column(String, nullable=True)
    sales = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    market = Column(Enum(Market), nullable=False)
    listings = relationship("Listing", back_populates="seller")
