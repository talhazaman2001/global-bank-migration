from fastapi import FastAPI, HTTPException
from typing import Optional
from pydantic import BaseModel
from datetime import datetime, timezone
import uuid

class TransactionBase(BaseModel):
    from_account: str
    to_account: str
    amount: float
    currency: str

class TransactionResponse(TransactionBase):
    transaction_id: str
    status: str
    timestamp: datetime

app = FastAPI()

@app.post("/transactions/", response_model=TransactionResponse)
async def create_transaction(txn: TransactionBase):
    return TransactionResponse(
        transaction_id=str(uuid.uuid4()),
        status="PENDING",
        timestamp=datetime.now(timezone.utc),
        **txn.model_dump()
    )

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "account"}