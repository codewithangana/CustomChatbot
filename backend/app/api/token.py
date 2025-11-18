from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.core.security import create_access_token

router = APIRouter()

class LoginRequest(BaseModel):
    username: str
    password: str

@router.post("/token")
def login(request: LoginRequest):
    # TODO: Replace with database check
    if request.username != "admin" or request.password != "admin123":
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": request.username})

    return {"access_token": token, "token_type": "bearer"}
