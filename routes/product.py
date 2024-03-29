from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from models.database import get_session
from schemas.core import MessageResponse
from schemas.products import (CreateNewProductRequest, GetAllProductsResponse,
                              Product, ProductToUpdate)
from schemas.user import User
from services.errors import ProducAlreadyExistError, ProducNotFoundError
from services.helpers import get_user_by_jwt
from services.products import (create_product, delete_a_product, get_a_product,
                               get_all_products, update_a_product)
from sqlalchemy.orm.session import Session

product_router = APIRouter(tags=["products"])


@product_router.post("/products")
async def handler_create_product(
    user: Annotated[User, Depends(get_user_by_jwt)],
    product: CreateNewProductRequest,
    session: Session = Depends(get_session),
) -> MessageResponse:
    try:
        create_product(session, product, user)

        return MessageResponse(message="Product successfully added")
    except ProducAlreadyExistError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e.message,
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@product_router.get("/products")
async def handler_get_all_products(
    session: Session = Depends(get_session),
) -> GetAllProductsResponse:
    try:
        products = get_all_products(session)

        return products
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@product_router.get("/products/{product_id}")
async def handler_get_a_product(
    product_id: int, session: Session = Depends(get_session)
) -> Product:
    try:
        return get_a_product(session, product_id)
    except ProducNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message,
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@product_router.delete("/products/{product_id}", status_code=status.HTTP_200_OK)
async def handler_delete_a_product(
    product_id: int,
    _: Annotated[User, Depends(get_user_by_jwt)],
    session: Session = Depends(get_session),
) -> MessageResponse:
    try:
        delete_a_product(session, product_id)

        return MessageResponse(message="Product deleted successfully")
    except ProducNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message,
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@product_router.patch("/products/{product_id}", status_code=status.HTTP_202_ACCEPTED)
async def handler_update_a_product(
    product_id: int,
    new_values: ProductToUpdate,
    _: Annotated[User, Depends(get_user_by_jwt)],
    session: Session = Depends(get_session),
) -> MessageResponse:
    try:
        update_a_product(session, product_id, new_values.as_dict())

        return MessageResponse(message="Product updated successfully")
    except ProducAlreadyExistError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e.message,
        )
    except ProducNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message,
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
