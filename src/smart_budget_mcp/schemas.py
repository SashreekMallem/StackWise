# src/smart_budget_mcp/schemas.py
from pydantic import BaseModel
from typing import List, Optional

class BudgetInput(BaseModel):
    monthly_limit: int

class CardNamesInput(BaseModel):
    card_names: List[str]

class WishlistItemInput(BaseModel):
    name: str
    urgency: Optional[str] = "not set"

class GroceryItemInput(BaseModel):
    name: str
    quantity: Optional[int] = 1
    frequency: Optional[str] = "weekly" 