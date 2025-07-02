from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from app.db.session import get_db
from app.models.receipt import Receipt
import pandas as pd
from fastapi.responses import StreamingResponse
from io import StringIO
from app.dependencies.admin_required import admin_required

router = APIRouter()


@router.get("/export-receipts")
def export_detailed_receipts(
    start_date: str = Query(..., example="2024-01-01"),
    end_date: str = Query(..., example="2024-12-31"),
    db: Session = Depends(get_db),
    current_user=Depends(admin_required)
):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not authorized")

    try:
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD.")

    receipts = db.query(Receipt).filter(
        Receipt.created_at >= start,
        Receipt.created_at <= end
    ).all()

    if not receipts:
        raise HTTPException(status_code=404, detail="No receipts found in this range")

    data = []

    for r in receipts:
        base = {
            "Receipt ID": r.id,
            "User ID": r.user_id,
            "Category": r.category,
            "File URL": r.file_url,
            "Created At": r.created_at.strftime("%Y-%m-%d %H:%M:%S"),
        }
        
        if r.category == "travel" and r.travel_details:
            travel = r.travel_details
            base.update({
                "From": travel.from_location,
                "To": travel.to_location,
                "Km": travel.kilometers,
                "Price": travel.price,
                "Mode": travel.mode_of_travel,
                "Custom Mode": travel.custom_mode
            })

      
        elif r.category == "food" and r.food_details:
            food = r.food_details
            base.update({
                "Food Type": food.food_type,
                "Restaurant": food.restaurant_name,
                "Amount": food.amount,
                "Notes": food.notes
            })

        
        elif r.category == "living" and r.living_details:
            living = r.living_details
            base.update({
                "Hotel": living.hotel_name,
                "Address": living.address,
                "Check-In": str(living.check_in_date),
                "Check-Out": str(living.check_out_date),
                "Amount": living.amount
            })

        elif r.category == "other" and r.other_details:
            other = r.other_details
            base.update({
                "Title": other.title,
                "Description": other.description,
                "Amount": other.amount
            })

        data.append(base)

    df = pd.DataFrame(data)
    csv_buffer = StringIO()
    df.to_csv(csv_buffer, index=False)
    csv_buffer.seek(0)

    return StreamingResponse(
        csv_buffer,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=receipts_detailed.csv"}
    )
