from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.api.auth import get_current_user
from app.schemas.receipt import (
    ReceiptCreate,
    TravelReceiptCreate,
    FoodReceiptCreate,
    LivingReceiptCreate,
    OtherReceiptCreate,
)
from app.crud.receipt import create_receipt
from app.core.drive import upload_file_to_drive
import json

router = APIRouter()


@router.post("/submit-receipt")
async def submit_receipt(
    file: UploadFile = File(...),
    category: str = Form(...),
    travel: str = Form(None),
    food: str = Form(None),
    living: str = Form(None),
    other: str = Form(None),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    # Step 1: Upload image to Google Drive
    try:
        file_url = await upload_file_to_drive(file)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {e}")

    # Step 2: Parse nested JSON fields
    travel_obj = TravelReceiptCreate(**json.loads(travel)) if travel else None
    food_obj = FoodReceiptCreate(**json.loads(food)) if food else None
    living_obj = LivingReceiptCreate(**json.loads(living)) if living else None
    other_obj = OtherReceiptCreate(**json.loads(other)) if other else None

    # Step 3: Build receipt schema
    receipt_data = ReceiptCreate(
        category=category,
        travel=travel_obj,
        food=food_obj,
        living=living_obj,
        other=other_obj,
    )

    # Step 4: Save to DB
    saved = create_receipt(
        db=db,
        user_id=current_user.id,
        file_url=file_url,
        receipt_data=receipt_data,
    )

    return {"message": "Receipt submitted successfully", "receipt_id": saved.id}
