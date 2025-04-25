from typing import List, Optional
from sqlalchemy.orm import Session

from app.models.image import Image, ImageTag
from app.schemas.image import ImageCreate, ImageUpdate


class ImageRepository:
    def create_image(self, db: Session, image_data: ImageCreate) -> Image:
        db_image = Image(
            image_url=image_data.image_url,
            title=image_data.title,
            author=image_data.author,
        )
        db.add(db_image)
        db.commit()
        db.refresh(db_image)

        # Create tags
        for tag in image_data.tags:
            db_tag = ImageTag(image_id=db_image.id, tag=tag)
            db.add(db_tag)
        
        db.commit()
        db.refresh(db_image)
        return db_image

    def get_images(
        self, 
        db: Session, 
        skip: int = 0, 
        limit: int = 100, 
        author: Optional[str] = None,
        tag: Optional[str] = None
    ) -> List[Image]:
        query = db.query(Image)
        
        if author:
            query = query.filter(Image.author == author)
        
        if tag:
            query = query.join(Image.tags).filter(ImageTag.tag == tag)
        
        return query.offset(skip).limit(limit).all()

    def get_image_by_id(self, db: Session, image_id: int) -> Optional[Image]:
        return db.query(Image).filter(Image.id == image_id).first()

    def update_image(self, db: Session, image_id: int, image_data: ImageUpdate) -> Optional[Image]:
        db_image = db.query(Image).filter(Image.id == image_id).first()
        if not db_image:
            return None

        # Update image attributes
        update_data = image_data.dict(exclude_unset=True)
        
        # Handle tags separately
        tags = update_data.pop("tags", None)
        
        for key, value in update_data.items():
            setattr(db_image, key, value)

        # Update tags if provided
        if tags is not None:
            # Delete existing tags
            db.query(ImageTag).filter(ImageTag.image_id == image_id).delete()
            
            # Create new tags
            for tag in tags:
                db_tag = ImageTag(image_id=image_id, tag=tag)
                db.add(db_tag)

        db.commit()
        db.refresh(db_image)
        return db_image

    def delete_image(self, db: Session, image_id: int) -> bool:
        db_image = db.query(Image).filter(Image.id == image_id).first()
        if not db_image:
            return False

        db.delete(db_image)
        db.commit()
        return True

    def export_images(
        self, 
        db: Session, 
        author: Optional[str] = None,
        tag: Optional[str] = None
    ) -> List[Image]:
        return self.get_images(db, skip=0, limit=10000, author=author, tag=tag)