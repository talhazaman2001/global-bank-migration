from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from typing import Optional
from pydantic import BaseModel
from datetime import datetime, timedelta, timezone

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    expires_at: datetime

app = FastAPI()

@app.post("/token", response_model=TokenResponse)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    if form_data.username != "test" or form_data.password != "test":
        raise HTTPException(status_code=401)
        
    return TokenResponse(
        access_token="sample_token",
        token_type="bearer",
        expires_at=datetime.now(timezone.utc) + timedelta(hours=1)
    )

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "account"}