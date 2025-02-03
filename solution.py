from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Dict
import uuid
import re
from math import ceil
import logging

logging.basicConfig(level=logging.INFO)

app = FastAPI(title="Receipt Processor", version="1.0.0")

receipts: Dict[str, dict] = {}

class Item(BaseModel):
    shortDescription: str = Field(..., pattern=r"^[\w\s\-]+$")
    price: str = Field(..., pattern=r"^\d+\.\d{2}$")

class Receipt(BaseModel):
    retailer: str = Field(..., pattern=r"^[\w\s\-\&]+$")
    purchaseDate: str = Field(..., pattern=r"^\d{4}-\d{2}-\d{2}$")
    purchaseTime: str = Field(..., pattern=r"^\d{2}:\d{2}$")
    items: List[Item] = Field(..., min_items=1)
    total: str = Field(..., pattern=r"^\d+\.\d{2}$")

def calculate_points(receipt: Receipt) -> int:
    points = 0
    points += sum(c.isalnum() for c in receipt.retailer)

    if re.match(r"^\d+\.00$", receipt.total):
        points += 50

    if float(receipt.total) % 0.25 == 0:
        points += 25

    points += (len(receipt.items) // 2) * 5

    for item in receipt.items:
        description_length = len(item.shortDescription.strip())
        if description_length % 3 == 0:
            price = float(item.price)
            points += ceil(price * 0.2)

    purchase_day = int(receipt.purchaseDate.split("-")[2])
    if purchase_day % 2 != 0:
        points += 6

    hour, minute = map(int, receipt.purchaseTime.split(":"))
    if 14 <= hour < 16:
        points += 10
        
    return points

@app.post("/receipts/process", response_model=dict)
async def process_receipt(receipt: Receipt):
    logging.info(f"Processing receipt with total {receipt.total} and retailer {receipt.retailer}")

    if re.match(r"^\d+$", receipt.retailer):
        raise HTTPException(
            status_code=400,
            detail="Retailer name cannot be purely numeric"
        )

    try:
        receipt_id = str(uuid.uuid4())
        receipts[receipt_id] = {
            "receipt": receipt,
            "points": calculate_points(receipt)
        }
        return {"id": receipt_id}
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Error processing receipt: {str(e)}"
        )
     

@app.get("/receipts/{id}/points", response_model=dict)
async def get_points(id: str):
    if id not in receipts:
        raise HTTPException(status_code=404, detail="No receipt found for that ID.")
    return {"points": receipts[id]["points"]}