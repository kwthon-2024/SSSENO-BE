from ninja import NinjaAPI
from .models import *
from .schemas import *
from typing import List
from django.shortcuts import get_object_or_404


api = NinjaAPI()

@api.post("total/professor/add",response=ProfessorResponseSchema)
def add_professor(request, professor: ProfessorResponseSchema):
    professor_obj = Professor.objects.create(**professor.dict())
    return professor_obj, {
        "message" : "교수 정보가 정상적으로 추가되었습니다."
    }

@api.put("total/professor/modify", response=ProfessorResponseSchema)
def update_professor(request, professor: ProfessorResponseSchema):
    professor_obj = get_object_or_404(Professor, id=professor.professor_id)
    update_data = professor.dict(exclude_unset=True)
    for attr, value in update_data.items():
        if value is not None and hasattr(professor_obj, attr):
            setattr(professor_obj, attr, value)
    professor_obj.save()
    return professor_obj, {
        "message" : "교수 정보가 정상적으로 수정되었습니다."
    }