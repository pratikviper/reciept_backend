from sqlalchemy.orm import Session
from app.models.receipt import Receipt
from app.models.travel import TravelReceipt
from app.models.food import FoodReceipt
from app.models.living import LivingReceipt
from app.models.other import OtherReceipt
from app.schemas.receipt import ReceiptCreate


def create_receipt(
    db: Session,
    user_id: int,
    file_url: str,
    receipt_data: ReceiptCreate
):
   
    receipt = Receipt(
        user_id=user_id,
        file_url=file_url,
        category=receipt_data.category
    )
    db.add(receipt)
    db.commit()
    db.refresh(receipt)


    if receipt_data.category == "travel" and receipt_data.travel:
        travel = receipt_data.travel
        travel_entry = TravelReceipt(
            receipt_id=receipt.id,
            from_location=travel.from_location,
            to_location=travel.to_location,
            kilometers=travel.kilometers,
            price=travel.price,
            mode_of_travel=travel.mode_of_travel,
            custom_mode=travel.custom_mode
        )
        db.add(travel_entry)

    elif receipt_data.category == "food" and receipt_data.food:
        food = receipt_data.food
        food_entry = FoodReceipt(
            receipt_id=receipt.id,
            food_type=food.food_type,
            restaurant_name=food.restaurant_name,
            amount=food.amount,
            notes=food.notes
        )
        db.add(food_entry)

    elif receipt_data.category == "living" and receipt_data.living:
        living = receipt_data.living
        living_entry = LivingReceipt(
            receipt_id=receipt.id,
            hotel_name=living.hotel_name,
            address=living.address,
            check_in_date=living.check_in_date,
            check_out_date=living.check_out_date,
            amount=living.amount
        )
        db.add(living_entry)

    elif receipt_data.category == "other" and receipt_data.other:
        other = receipt_data.other
        other_entry = OtherReceipt(
            receipt_id=receipt.id,
            title=other.title,
            description=other.description,
            amount=other.amount
        )
        db.add(other_entry)

    db.commit()
    return receipt
