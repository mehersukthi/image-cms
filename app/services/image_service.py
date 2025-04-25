from typing import List, Optional
from sqlalchemy.orm import Session

from app.repositories.image_repository import ImageRepository
from app.schemas.image import ImageCreate, ImageUpdate, Image, ImageSummary


class ImageService:
    def __init__(self):
        self.repository = ImageRepository()

    def create_image(self, db: Session, image_data: ImageCreate) -> Image:
        return self.repository.create_image(db, image_data)

    def get_images(
        self, 
        db: Session, 
        skip: int = 0, 
        limit: int = 100, 
        author: Optional[str] = None,
        tag: Optional[str] = None
    ) -> List[ImageSummary]:
        images = self.repository.get_images(db, skip, limit, author, tag)
        result = []
        
        for image in images:
            tags = [tag.tag for tag in image.tags]
            result.append(
                ImageSummary(
                    id=image.id,
                    title=image.title,
                    author=image.author,
                    tags=tags,
                    created_at=image.created_at
                )
            )
        
        return result

    def get_image_by_id(self, db: Session, image_id: int) -> Optional[Image]:
        return self.repository.get_image_by_id(db, image_id)

    def update_image(self, db: Session, image_id: int, image_data: ImageUpdate) -> Optional[Image]:
        return self.repository.update_image(db, image_id, image_data)

    def delete_image(self, db: Session, image_id: int) -> bool:
        return self.repository.delete_image(db, image_id)

    def export_images(
        self, 
        db: Session, 
        author: Optional[str] = None,
        tag: Optional[str] = None
    ) -> List[Image]:
        return self.repository.export_images(db, author, tag)