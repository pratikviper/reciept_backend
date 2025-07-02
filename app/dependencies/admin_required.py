from fastapi import Depends, HTTPException
from app.api.auth import get_current_user

def admin_required(current_user = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access only")
    return current_user
