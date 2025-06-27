from sqlalchemy import Column, Integer, Float, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.session import Base

class FoodReceipt(Base):
    __tablename__ = "food_receipts"

    id = Column(Integer, primary_key=True, index=True)
    receipt_id = Column(Integer, ForeignKey("receipts.id"))

    food_type = Column(String, nullable=False)
    restaurant_name = Column(String, nullable=True)
    amount = Column(Float, nullable=False)
    notes = Column(String, nullable=True)

    receipt = relationship("Receipt", back_populates="food_details")
