from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from typing import Optional
from pydantic import BaseModel
from datetime import datetime, timezone
import uuid

class AccountBase(BaseModel):
    customer_id: str
    account_type: str
    currency: str
    balance: float

class AccountResponse(AccountBase):
    account_id: str
    created_at: datetime
    status: str

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.post("/accounts/", response_model=AccountResponse)
async def create_account(account: AccountBase):
    account_id = str(uuid.uuid4())
    return AccountResponse(
        account_id=account_id,
        created_at=datetime.now(timezone.utc),
        status="ACTIVE",
        **account.model_dump()
    )

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "account"}
