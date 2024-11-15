from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel

# PaginatedResponse가 Pydantic 모델로 정의되어 있다고 가정
class PaginatedResponse(BaseModel):
    total_pages: int
    current_page: int
    total_count: int
    results: list
    class Config:
        from_attributes = True

class RecommendedSchema(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True


class UserSchema(BaseModel):
    id: int
    username: str
    email: Optional[str] = None
    class Config:
        from_attributes = True

class ComplaintFormSchema(BaseModel):
    complaint_id: int
    complaint_title: str
    description: Optional[str] = ""
    accepted: Optional[bool] = False
    gachucount: Optional[int] = 0
    category: str
    answer: Optional[str] = None
    created: Optional[datetime] = None  # datetime 객체로 처리

    class Config:
        from_attributes = True
# 페이지스키마
