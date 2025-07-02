from fastapi import FastAPI
from app.api import auth, receipt, admin

app = FastAPI()

app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(receipt.router, prefix="/receipts", tags=["Receipts"])
app.include_router(admin.router, prefix="/admin", tags=["Admin"])
