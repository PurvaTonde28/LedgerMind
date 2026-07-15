from pydantic import BaseModel, Field 


class Transaction(BaseModel):
    date: str      # ISO format after cleaning (YYYY-MM-DD)
    description: str
    amount: float     # positive for expense, negative for income? We'll keep as is.
    raw_category: str = Field(default="uncategorized")