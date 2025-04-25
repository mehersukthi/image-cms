from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.image import Image
from app.services.image_service import ImageService

router = APIRouter()
image_service = ImageService()


@router.get("/export/", response_model=List[Image])
def export_images(
    author: Optional[str] = None, 
    tag: Optional[str] = None,
    db: Session = Depends(get_db)
):
    return image_service.export_images(db, author, tag)