from typing import List, Optional
import grpc
from sqlalchemy.orm import Session
from google.protobuf.timestamp_pb2 import Timestamp

import image_service_pb2 as pb2
import image_service_pb2_grpc as pb2_grpc
from app.db.session import SessionLocal
from app.services.image_service import ImageService
from app.schemas.image import ImageCreate, ImageUpdate


class ImageServiceServicer(pb2_grpc.ImageServiceServicer):
    def __init__(self):
        self.image_service = ImageService()

    def _get_db(self):
        db = SessionLocal()
        try:
            return db
        finally:
            db.close()

    def _convert_datetime_to_timestamp(self, dt):
        timestamp = Timestamp()
        timestamp.FromDatetime(dt)
        return timestamp

    def ListImages(self, request, context):
        db = self._get_db()
        images = self.image_service.get_images(
            db=db,
            skip=request.skip,
            limit=request.limit,
            author=request.author if request.HasField("author") else None,
            tag=request.tag if request.HasField("tag") else None
        )
        
        response = pb2.ListImagesResponse()
        for image in images:
            image_summary = response.images.add()
            image_summary.id = image.id
            image_summary.title = image.title
            image_summary.author = image.author
            image_summary.tags.extend(image.tags)
            image_summary.created_at.CopyFrom(self._convert_datetime_to_timestamp(image.created_at))
        
        return response

    def GetImage(self, request, context):
        db = self._get_db()
        image = self.image_service.get_image_by_id(db, request.image_id)
        
        if not image:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('Image not found')
            return pb2.ImageResponse()
        
        response = pb2.ImageResponse()
        image_detail = pb2.ImageDetail()
        image_detail.id = image.id
        image_detail.image_url = image.image_url
        image_detail.title = image.title
        image_detail.author = image.author
        image_detail.tags.extend([tag.tag for tag in image.tags])
        image_detail.created_at.CopyFrom(self._convert_datetime_to_timestamp(image.created_at))
        
        response.image.CopyFrom(image_detail)
        return response

    def CreateImage(self, request, context):
        db = self._get_db()
        image_data = ImageCreate(
            image_url=request.image_url,
            title=request.title,
            author=request.author,
            tags=list(request.tags)
        )
        
        image = self.image_service.create_image(db, image_data)
        
        response = pb2.ImageResponse()
        image_detail = pb2.ImageDetail()
        image_detail.id = image.id
        image_detail.image_url = image.image_url
        image_detail.title = image.title
        image_detail.author = image.author
        image_detail.tags.extend([tag.tag for tag in image.tags])
        image_detail.created_at.CopyFrom(self._convert_datetime_to_timestamp(image.created_at))
        
        response.image.CopyFrom(image_detail)
        return response

    def UpdateImage(self, request, context):
        db = self._get_db()
        
        # Prepare update data
        update_data = {}
        if request.HasField("image_url"):
            update_data["image_url"] = request.image_url
        if request.HasField("title"):
            update_data["title"] = request.title
        if request.HasField("author"):
            update_data["author"] = request.author
        if request.tags:
            update_data["tags"] = list(request.tags)
        
        image_data = ImageUpdate(**update_data)
        image = self.image_service.update_image(db, request.image_id, image_data)
        
        if not image:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('Image not found')
            return pb2.ImageResponse()
        
        response = pb2.ImageResponse()
        image_detail = pb2.ImageDetail()
        image_detail.id = image.id
        image_detail.image_url = image.image_url
        image_detail.title = image.title
        image_detail.author = image.author
        image_detail.tags.extend([tag.tag for tag in image.tags])
        image_detail.created_at.CopyFrom(self._convert_datetime_to_timestamp(image.created_at))
        
        response.image.CopyFrom(image_detail)
        return response

    def DeleteImage(self, request, context):
        db = self._get_db()
        success = self.image_service.delete_image(db, request.image_id)
        
        if not success:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('Image not found')
        
        return pb2.DeleteImageResponse(success=success)

    def ExportImages(self, request, context):
        db = self._get_db()
        images = self.image_service.export_images(
            db=db,
            author=request.author if request.HasField("author") else None,
            tag=request.tag if request.HasField("tag") else None
        )
        
        response = pb2.ExportImagesResponse()
        for image in images:
            image_detail = response.images.add()
            image_detail.id = image.id
            image_detail.image_url = image.image_url
            image_detail.title = image.title
            image_detail.author = image.author
            image_detail.tags.extend([tag.tag for tag in image.tags])
            image_detail.created_at.CopyFrom(self._convert_datetime_to_timestamp(image.created_at))
        
        return response