from pydantic import BaseModel
from typing import Optional

class UserAuthenticationRequestSchema(BaseModel):
    name: str
    birthday: str
    gubun: Optional[str] = None
    codeName1: Optional[str] = None
    sex: Optional[str] = None
    hakbun: Optional[str] = None

    class Config:
        orm_mode = True
