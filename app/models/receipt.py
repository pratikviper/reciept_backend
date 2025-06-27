from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.session import Base

class Receipt(Base):
    __tablename__ = "receipts"

    id = Column(Integer, primary_key=True, index=True)
    file_url = Column(String, nullable=False)
    category = Column(String, nullable=False)  # e.g., travel, food, etc.
    user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User")

    travel_details = relationship("TravelReceipt", back_populates="receipt", uselist=False)
    food_details = relationship("FoodReceipt", back_populates="receipt", uselist=False)
    living_details = relationship("LivingReceipt", back_populates="receipt", uselist=False)
    other_details = relationship("OtherReceipt", back_populates="receipt", uselist=False)
