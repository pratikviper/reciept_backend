from sqlalchemy import Column, Integer, Float, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.session import Base

class TravelReceipt(Base):
    __tablename__ = "travel_receipts"

    id = Column(Integer, primary_key=True, index=True)
    receipt_id = Column(Integer, ForeignKey("receipts.id"))

    from_location = Column(String, nullable=False)
    to_location = Column(String, nullable=False)
    kilometers = Column(Float, nullable=False)
    price = Column(Float, nullable=False)
    mode_of_travel = Column(String, nullable=False)  # e.g., "ola", "bus", "other"
    custom_mode = Column(String, nullable=True)

    receipt = relationship("Receipt", back_populates="travel_details")
