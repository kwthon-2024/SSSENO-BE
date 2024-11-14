from pydantic import BaseModel
from ninja import Schema
from datetime import datetime

class SearchRequestSchema(Schema):
    building_title: str
    capacity_max: int

class SearchfilterRequestSchema(BaseModel):
    building_title: str
    capacity_max: int
    type: str
    has_projector: bool
    has_mic: bool
    desk_type: str

class ClassroomSchema(BaseModel):
    Building_title: str
    Place_title: str
    capacity: int
    rating: float

class PaginationInfo(BaseModel):
    current_page: int
    per_page: int
    total_items: int
    total_pages: int

class ClassroomListResponse(BaseModel):
    success: bool
    data: dict
    pagination: PaginationInfo

class ClassroomDetailRequestSchema(BaseModel):
    building_name: str
    place_name: str


class ClassroomDetailResponseSchema(BaseModel):
    building_name: str
    place_name: str
    capacity: int
    rating: float

    
class ClassroomCreateRequestSchema(BaseModel):
    image_id: str
    building_name: str
    capacity_min: int
    place_name: str
    rating: float
    description: str
    type: str
    has_projector: bool
    has_mic: bool
    has_clock: bool
    desk_type: str
    reserved_time: datetime #추후 수정(빼야함)
    reserved: bool #추후 수정(뺴야함)

class ClassroomCreateResponseSchema(BaseModel):
    success: bool
    message: str
    data: dict

class ClassroomDeleteRequestSchema(BaseModel):
    building_name: str
    place_name: str

class ClassroomDeleteResponseSchema(BaseModel):
    success: bool
    message: str

class ClassroomMoreDetailRequestSchema(BaseModel):
    building_name: str
    place_name: str

class ClassroomMoreDetailResponseSchema(BaseModel):
    image_id: str
    building_name: str
    capacity: int
    place_name: str
    rating: float
    description: str
    type: str
    has_projector: bool
    has_mic: bool
    desk_type: str
    reserved: bool 
    