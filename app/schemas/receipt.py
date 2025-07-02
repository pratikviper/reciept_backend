from pydantic import BaseModel
from datetime import datetime, date
from typing import Optional


class TravelReceiptCreate(BaseModel):
    from_location: str
    to_location: str
    kilometers: float
    price: float
    mode_of_travel: str
    custom_mode: Optional[str] = None

class TravelReceiptOut(TravelReceiptCreate):
    pass


class FoodReceiptCreate(BaseModel):
    food_type: str            
    restaurant_name: Optional[str] = None
    amount: float
    notes: Optional[str] = None

class FoodReceiptOut(FoodReceiptCreate):
    pass


class LivingReceiptCreate(BaseModel):
    hotel_name: str
    address: Optional[str] = None
    check_in_date: Optional[date] = None
    check_out_date: Optional[date] = None
    amount: float

class LivingReceiptOut(LivingReceiptCreate):
    pass


class OtherReceiptCreate(BaseModel):
    title: str
    description: Optional[str] = None
    amount: float

class OtherReceiptOut(OtherReceiptCreate):
    pass


class ReceiptCreate(BaseModel):
    category: str                         
    travel: Optional[TravelReceiptCreate] = None
    food: Optional[FoodReceiptCreate] = None
    living: Optional[LivingReceiptCreate] = None
    other: Optional[OtherReceiptCreate] = None


class ReceiptOut(BaseModel):
    id: int
    file_url: str
    category: str
    user_id: int
    created_at: datetime

    travel_details: Optional[TravelReceiptOut] = None
    food_details: Optional[FoodReceiptOut] = None
    living_details: Optional[LivingReceiptOut] = None
    other_details: Optional[OtherReceiptOut] = None

    class Config:
        orm_mode = True
