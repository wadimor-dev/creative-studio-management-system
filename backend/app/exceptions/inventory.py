from fastapi import status
from app.core.exceptions import AppException

class InventoryException(AppException):
    pass

class StockEmptyException(InventoryException):
    def __init__(self, message="Stock is empty or insufficient"):
        super().__init__(message=message, status_code=status.HTTP_400_BAD_REQUEST)

class ItemNotFoundException(InventoryException):
    def __init__(self, message="Item not found"):
        super().__init__(message=message, status_code=status.HTTP_404_NOT_FOUND)

class InvalidQuantityException(InventoryException):
    def __init__(self, message="Invalid quantity"):
        super().__init__(message=message, status_code=status.HTTP_400_BAD_REQUEST)
