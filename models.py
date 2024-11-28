from dataclasses import dataclass
from typing import List
from datetime import date, time

@dataclass
class Item:
    short_description: str
    price: float

@dataclass
class Receipt:
    retailer: str
    purchase_date: date
    purchase_time: time
    items: List[Item]
    total: float