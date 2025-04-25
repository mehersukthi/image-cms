from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel


class TagBase(BaseModel):
    tag: str


class TagCreate(TagBase):
    pass


class Tag(TagBase):
    id: int
    image_id: int

    class Config:
        orm_mode = True


class ImageBase(BaseModel):
    title: str
    author: str
    image_url: str


class ImageCreate(ImageBase):
    tags: List[str]


class ImageUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    image_url: Optional[str] = None
    tags: Optional[List[str]] = None


class Image(ImageBase):
    id: int
    created_at: datetime
    tags: List[Tag]

    class Config:
        orm_mode = True


class ImageSummary(BaseModel):
    id: int
    title: str
    author: str
    tags: List[str]
    created_at: datetime

    class Config:
        orm_mode = True