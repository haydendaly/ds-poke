from enum import Enum

from sqlalchemy import Column, DateTime, Enum, Float, ForeignKey, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .base import Base
from .enums.listing_status import ListingStatus
from .enums.market import Market


class Listing(Base):
    __tablename__ = "listing"

    item_id = Column(String, primary_key=True)
    market = Column(Enum(Market), nullable=False)
    title = Column(String, nullable=False)
    thumbnail_url = Column(String, nullable=True)
    price = Column(Float, nullable=True)
    image_urls = Column(
        String, nullable=True
    )  # You can store this as a comma-separated string, or use a custom type
    raw_image_urls = Column(String, nullable=False)
    description = Column(String, nullable=False)
    url = Column(String, nullable=False)
    status = Column(Enum(ListingStatus), nullable=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    seller_id = Column(String, ForeignKey("seller.id"))
    seller = relationship("Seller", back_populates="listings")
