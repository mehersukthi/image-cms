from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.image import ImageCreate, ImageUpdate, Image, ImageSummary
from app.services.image_service import ImageService

router = APIRouter()
image_service = ImageService()


@router.post("/images/", response_model=Image, status_code=201)
def create_image(image: ImageCreate, db: Session = Depends(get_db)):
    return image_service.create_image(db, image)


@router.get("/images/", response_model=List[ImageSummary])
def list_images(
    skip: int = 0, 
    limit: int = 100, 
    author: Optional[str] = None, 
    tag: Optional[str] = None,
    db: Session = Depends(get_db)
):
    images = image_service.get_images(db, skip, limit, author, tag)
    return images


@router.get("/images/{image_id}", response_model=Image)
def get_image(image_id: int, db: Session = Depends(get_db)):
    image = image_service.get_image_by_id(db, image_id)
    if image is None:
        raise HTTPException(status_code=404, detail="Image not found")
    return image


@router.put("/images/{image_id}", response_model=Image)
def update_image(image_id: int, image_data: ImageUpdate, db: Session = Depends(get_db)):
    image = image_service.update_image(db, image_id, image_data)
    if image is None:
        raise HTTPException(status_code=404, detail="Image not found")
    return image


@router.delete("/images/{image_id}", status_code=204)
def delete_image(image_id: int, db: Session = Depends(get_db)):
    success = image_service.delete_image(db, image_id)
    if not success:
        raise HTTPException(status_code=404, detail="Image not found")
    return {"detail": "Image deleted"}