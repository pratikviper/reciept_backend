from fastapi import FastAPI
from app.api import auth, receipts, admin

app = FastAPI()

app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(receipts.router, prefix="/receipts", tags=["Receipts"])
app.include_router(admin.router, prefix="/admin", tags=["Admin"])
