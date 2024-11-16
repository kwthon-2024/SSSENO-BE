from datetime import datetime
from typing import Optional, List

from django.db.models import AutoField
from pydantic import BaseModel

# PaginatedResponse가 Pydantic 모델로 정의되어 있다고 가정
from typing import List, Optional
class PaginatedResponse(BaseModel):
    total_pages: int
    current_page: int
    total_count: int
    results: Optional[List] = None  # results를 선택적 필드로 설정 (기본값 None)

    class Config:
        from_attributes = True

class RecommendedSchema(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True

class ComplaintSearchSchema(BaseModel):
    complaint_title : Optional[str] = ''
    description : Optional[str] = ''
    accepted: Optional[bool] = None  # False나 True
    page: int = 1  # 페이지 번호, 기본값 1
    kw: Optional[str] = ''  # 검색어, 기본값은 빈 문자열
    search_type: str = 'both'  # 검색 타입: 'title', 'description', 'both'
    category: Optional[str] = ''  # 카테고리, 기본값은 빈 문자열

class UserSchema(BaseModel):
    id: int
    username: str
    email: Optional[str] = None
    class Config:
        from_attributes = True

class ComplaintFormSchema(BaseModel):
    complaint_id : int
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
