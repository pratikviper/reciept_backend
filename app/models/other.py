from sqlalchemy import Column, Integer, Float, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.session import Base

class OtherReceipt(Base):
    __tablename__ = "other_receipts"

    id = Column(Integer, primary_key=True, index=True)
    receipt_id = Column(Integer, ForeignKey("receipts.id"))

    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    amount = Column(Float, nullable=False)

    receipt = relationship("Receipt", back_populates="other_details")
