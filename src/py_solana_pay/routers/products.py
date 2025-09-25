"""Product management router"""

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from ..database import get_db
from ..models.product import Product
from .auth import get_current_user

router = APIRouter()

# Dependency injection variables
db_dependency = Depends(get_db)
current_user_dependency = Depends(get_current_user)


class ProductBase(BaseModel):
    name: str
    price: float
    image: Optional[str] = None
    quantity: int = 0


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    image: Optional[str] = None
    quantity: Optional[int] = None


class ProductResponse(ProductBase):
    id: int

    class Config:
        from_attributes = True


@router.get("/", response_model=List[ProductResponse])
async def get_products(skip: int = 0, limit: int = 100, db: Session = db_dependency):
    """Get all products"""
    products = db.query(Product).offset(skip).limit(limit).all()
    return products


@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(product_id: int, db: Session = db_dependency):
    """Get product by ID"""
    product = db.query(Product).filter(Product.id == product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.post("/", response_model=ProductResponse)
async def create_product(
    product: ProductCreate,
    db: Session = db_dependency,
    current_user = current_user_dependency,
):
    """Create new product (authenticated users only)"""
    db_product = Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


@router.put("/{product_id}", response_model=ProductResponse)
async def update_product(
    product_id: int,
    product_update: ProductUpdate,
    db: Session = db_dependency,
    current_user = current_user_dependency,
):
    """Update product (authenticated users only)"""
    product = db.query(Product).filter(Product.id == product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    update_data = product_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(product, field, value)

    db.commit()
    db.refresh(product)
    return product


@router.delete("/{product_id}")
async def delete_product(
    product_id: int,
    db: Session = db_dependency,
    current_user = current_user_dependency,
):
    """Delete product (authenticated users only)"""
    product = db.query(Product).filter(Product.id == product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    db.delete(product)
    db.commit()
    return {"message": "Product deleted successfully"}
