from pydantic import BaseModel
from typing import List
from app.schemas.inventory import TransactionResponse
from typing import Any, Dict

class DashboardMetrics(BaseModel):
    total_items: int
    total_products: int
    total_stock: int
    total_product_stock: int
    todays_activity: int
    recent_transactions: List[Dict[str, Any]]
    chart_data: List[Dict[str, Any]]
    quick_summary: List[Dict[str, str]]
