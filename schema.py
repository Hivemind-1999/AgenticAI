from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class VegasEvent(BaseModel):
    name: str
    venue: str
    start_time: datetime  # Changed from string to datetime
    category: str
    link: Optional[str] = None
    insider_tip: Optional[str] = "Check description for details"
    price: Optional[str] = "Free" # Add this line