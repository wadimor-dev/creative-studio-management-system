from typing import Optional
from sqlalchemy.orm import Session
from app.repositories.base_repository import BaseRepository
from app.models.inventory_transaction import InventoryTransaction
from app.schemas.inventory import TransactionCreate, TransactionUpdate

class InventoryTransactionRepository(BaseRepository[InventoryTransaction, TransactionCreate, TransactionUpdate]):
    def __init__(self):
        super().__init__(InventoryTransaction)

inventory_transaction_repo = InventoryTransactionRepository()
