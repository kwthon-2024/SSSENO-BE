from pydantic import BaseModel
from typing import List

# Subject에 대한 스키마
class SubjectSchema(BaseModel):
    subject_name1: str
    subject_name2: str
    subject_name3: str

# Info에 대한 스키마
class Info(BaseModel):
    number: str
    lab: str
    email: str
    subject: List[SubjectSchema]

# 새로운 Reputation 스키마
class ReputationSchema(BaseModel):
    reputation1_st : str
    reputation1_per: int
    reputation2_st : str
    reputation2_per: int
    reputation3_st : str
    reputation3_per: int
    reputation4_st : str
    reputation4_per: int
    reputation5_st : str
    reputation5_per: int

# 최종 반환할 교수 정보 스키마
class ProfessorResponseSchema(BaseModel):
    professor_id: int
    professor_name: str
    college: str
    department: str
    description: str
    professor_photo: str
    info: List[Info]
    reputation: List[ReputationSchema]

    class Config:
        orm_mode = True
