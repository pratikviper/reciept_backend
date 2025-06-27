from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.db.session import get_db
from app.schemas.user import UserCreate, UserOut
from app.crud.user import create_user, get_user_by_email
from app.core.security import verify_password, create_access_token
from datetime import timedelta

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

@router.post("/register", response_model=UserOut)
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return create_user(db, user)

@router.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = get_user_by_email(db, form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    access_token = create_access_token(data={"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    from app.models.user import User
    from app.core.security import decode_access_token

    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    user_id = payload.get("sub")
    user = db.query(User).filter(User.id == int(user_id)).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user
