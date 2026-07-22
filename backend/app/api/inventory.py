from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from typing import Optional

from app.core.database.session import get_db

from app.common.responses import (
    SuccessResponse,
    create_success_response,
)

from app.common.pagination import (
    PaginationParams,
    PaginatedResponse,
    create_paginated_response,
)

from app.schemas.item import (
    ItemCreate,
    ItemUpdate,
    ItemResponse,
)

from app.schemas.inventory import (
    TransactionCreate,
    TransactionResponse,
)

from app.services.item_service import item_service
from app.services.inventory_service import inventory_service

from app.dependencies.auth import get_current_user
from app.dependencies.permission import RequirePermission

from app.constants.permissions import Permission

router = APIRouter()

# =============================================================================
# ITEMS
# =============================================================================

@router.get(
    "/items",
    response_model=PaginatedResponse[ItemResponse],
    dependencies=[
        Depends(
            RequirePermission(
                Permission.INVENTORY_VIEW
            )
        )
    ]
)
def list_items(
    params: PaginationParams = Depends(),
    search: Optional[str] = None,
    category_id: Optional[int] = Query(None),
    location_id: Optional[int] = Query(None),
    db: Session = Depends(get_db),
):

    items, total = item_service.get_items(
        db=db,
        skip=params.skip,
        limit=params.size,
        search=search,
        category_id=category_id,
        location_id=location_id,
    )

    return create_paginated_response(
        data=items,
        total=total,
        page=params.page,
        size=params.size,
    )


@router.post(
    "/items",
    response_model=SuccessResponse[ItemResponse],
    status_code=status.HTTP_201_CREATED,
    dependencies=[
        Depends(
            RequirePermission(
                Permission.INVENTORY_CREATE
            )
        )
    ]
)
def create_item(
    item_in: ItemCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):

    item = item_service.create_item(
        db=db,
        item_in=item_in,
        user_id=current_user.id,
    )

    return create_success_response(
        data=item,
        message="Item created successfully",
    )


@router.get(
    "/items/{item_id}",
    response_model=SuccessResponse[ItemResponse],
    dependencies=[
        Depends(
            RequirePermission(
                Permission.INVENTORY_VIEW
            )
        )
    ]
)
def get_item(
    item_id: int,
    db: Session = Depends(get_db),
):

    item = item_service.get_item(
        db,
        item_id,
    )

    return create_success_response(
        data=item,
        message="Item fetched successfully",
    )


@router.put(
    "/items/{item_id}",
    response_model=SuccessResponse[ItemResponse],
    dependencies=[
        Depends(
            RequirePermission(
                Permission.INVENTORY_UPDATE
            )
        )
    ]
)
def update_item(
    item_id: int,
    item_in: ItemUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):

    item = item_service.update_item(
        db=db,
        item_id=item_id,
        item_in=item_in,
        user_id=current_user.id,
    )

    return create_success_response(
        data=item,
        message="Item updated successfully",
    )


@router.delete(
    "/items/{item_id}",
    response_model=SuccessResponse[dict],
    dependencies=[
        Depends(
            RequirePermission(
                Permission.INVENTORY_DELETE
            )
        )
    ]
)
def delete_item(
    item_id: int,
    db: Session = Depends(get_db),
):

    item_service.delete_item(
        db,
        item_id,
    )

    return create_success_response(
        data=None,
        message="Item deleted successfully",
    )


# =============================================================================
# TRANSACTIONS
# =============================================================================

@router.get(
    "/transactions",
    response_model=PaginatedResponse[TransactionResponse],
    dependencies=[
        Depends(
            RequirePermission(
                Permission.INVENTORY_TRANSACTION_VIEW
            )
        )
    ]
)
def list_transactions(
    params: PaginationParams = Depends(),
    item_id: Optional[int] = Query(None),
    user_id: Optional[int] = Query(None),
    category_id: Optional[int] = Query(None),
    location_id: Optional[int] = Query(None),
    type: Optional[str] = Query(None),
    db: Session = Depends(get_db),
):

    transactions, total = inventory_service.get_transaction_history(
        db=db,
        skip=params.skip,
        limit=params.size,
        item_id=item_id,
        user_id=user_id,
        type=type,
        category_id=category_id,
        location_id=location_id,
    )

    return create_paginated_response(
        data=transactions,
        total=total,
        page=params.page,
        size=params.size,
    )


@router.post(
    "/transactions",
    response_model=SuccessResponse[TransactionResponse],
    status_code=status.HTTP_201_CREATED,
    dependencies=[
        Depends(
            RequirePermission(
                Permission.INVENTORY_TRANSACTION_CREATE
            )
        )
    ]
)
def create_transaction(
    tx_in: TransactionCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):

    transaction = inventory_service.process_transaction(
        db=db,
        user_id=current_user.id,
        tx_in=tx_in,
    )

    return create_success_response(
        data=transaction,
        message="Transaction processed successfully",
    )