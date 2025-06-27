from sqlalchemy import Column, Integer, Float, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.db.session import Base

class LivingReceipt(Base):
    __tablename__ = "living_receipts"

    id = Column(Integer, primary_key=True, index=True)
    receipt_id = Column(Integer, ForeignKey("receipts.id"))

    hotel_name = Column(String, nullable=False)
    address = Column(String, nullable=True)
    check_in_date = Column(Date, nullable=True)
    check_out_date = Column(Date, nullable=True)
    amount = Column(Float, nullable=False)

    receipt = relationship("Receipt", back_populates="living_details")
