from pydantic import BaseModel
from ninja import NinjaAPI, Schema
from typing import List, Optional


class InfoCreateSchema(BaseModel):
    professor: str
    college: str
    department: str
    description: str
    photo: str
    number: str
    lab: str
    email: str
    subject1: str
    subject2: str
    subject3: str

    class Config:
        from_attributes=True

class IdSchema(Schema):
    id: int

class ProfessorSearchSchema(Schema):
    professor: Optional[str] = ''  # 교수 이름을 받기 위한 필드professor: str  # 교수 이름을 받을 필드
    college : Optional[str] = ''
    department : Optional[str] = ''
    page: Optional[int] = 1  # 페이지 번호, 기본값은 1
    page_size: Optional[int] = 10  # 페이지 크기, 기본값은 10

    class Config:
        # 이 설정을 통해 ORM 모델을 사용한 변환이 가능하도록 함
        from_attributes = True

# 수정용 스키마 정의 (필요한 필드만 포함)
class InfoUpdateSchema(Schema):
    id: int  # 수정할 항목의 id를 포함
    professor: str
    college: str
    department: str
    description: str
    photo: str
    number: str
    lab: str
    email: str
    subject1: str
    subject2: str
    subject3: str
    class Config:
        from_attributes=True

class ProfessorOut(BaseModel):
    id: int
    professor: str
    college: str
    department: str
    description: Optional[str] = None
    photo: Optional[str] = None
    number: Optional[str] = None
    lab: Optional[str] = None
    email: Optional[str] = None
    subject1: Optional[str] = None
    subject2: Optional[str] = None
    subject3: Optional[str] = None

    class Config:
        from_attributes = True

class RepuUpdateSchema(Schema):
    id: int          # `id`를 요청 본문에 포함
    repu1: str
    repu2: str
    repu3: str
    repu4: str
    repu5: str

class SubjectSearchSchema(BaseModel):
    Subject: str