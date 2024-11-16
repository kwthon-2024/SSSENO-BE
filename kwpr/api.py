from ninja import NinjaAPI, Schema
from .models import *
from .schemas import *
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q

api3 = NinjaAPI()

# POST 요청 처리 (JSON 데이터를 받아서 DB에 저장)
@api3.post("/total/professor/add", response=InfoCreateSchema)
def create_info(request, data: InfoCreateSchema):
    # 각 필드를 일대일로 대응하여 데이터베이스에 저장
    info = Info.objects.create(
        professor=data.professor,
        college=data.college,
        department=data.department,
        description=data.description,
        photo=data.photo,
        number=data.number,
        lab=data.lab,
        email=data.email,
        subject1=data.subject1,
        subject2=data.subject2,
        subject3=data.subject3,
    )


    return InfoCreateSchema.from_orm(info)



@api3.put("/total/professor/evaluate")
def update_repu(request, payload: RepuUpdateSchema):
    try:
        # `id`에 해당하는 Repu 객체 가져오기
        repu_instance = Info.objects.get(id=payload.id)
    except Info.DoesNotExist:
        return {"error": "Repu with the given id does not exist"}

    # 매핑 테이블
    REPU_MAPPING = {
        "예시좌강": -100,
        "예시좌약": -50,
        "예시보통": 0,
        "예시우약": 50,
        "예시우강": 100,
    }

    # 매핑 값 가져오기 및 기존 값에 더하기
    repu_instance.repu1 += REPU_MAPPING.get(payload.repu1, 0)
    repu_instance.repu2 += REPU_MAPPING.get(payload.repu2, 0)
    repu_instance.repu3 += REPU_MAPPING.get(payload.repu3, 0)
    repu_instance.repu4 += REPU_MAPPING.get(payload.repu4, 0)
    repu_instance.repu5 += REPU_MAPPING.get(payload.repu5, 0)

    # count 증가
    repu_instance.count += 1

    # 변경 내용 저장
    repu_instance.save()

    count = repu_instance.count
    repu_per1 = repu_instance.repu1 / count if count > 0 else 0.0
    repu_per2 = repu_instance.repu2 / count if count > 0 else 0.0
    repu_per3 = repu_instance.repu3 / count if count > 0 else 0.0
    repu_per4 = repu_instance.repu4 / count if count > 0 else 0.0
    repu_per5 = repu_instance.repu5 / count if count > 0 else 0.0


    return {
        "id": repu_instance.id,
        "repu1": repu_instance.repu1,
        "repu2": repu_instance.repu2,
        "repu3": repu_instance.repu3,
        "repu4": repu_instance.repu4,
        "repu5": repu_instance.repu5,
        "count": repu_instance.count,
        "repu_per1": round(repu_per1, 2),
        "repu_per2": round(repu_per2, 2),
        "repu_per3": round(repu_per3, 2),
        "repu_per4": round(repu_per4, 2),
        "repu_per5": round(repu_per5, 2),
    }


@api3.get("/total/professor/detail", response=InfoCreateSchema)
def get_info_by_id(request, data: IdSchema):
    try:
        # 요청 본문에서 받은 id 값으로 Info 객체 조회
        info = Info.objects.get(id=data.id)
    except Info.DoesNotExist:
        # 해당 ID가 없을 경우 404 응답
        return JsonResponse({"error": "Info with the given id does not exist"}, status=404)
    
    # 조회된 Info 객체 반환
    return InfoCreateSchema.from_orm(info)

@api3.post("/total/professor/delete", response={200: str, 404: str})
def delete_info_by_id(request, data: IdSchema):
    try:
        # 요청 본문에서 받은 id 값으로 Info 객체 조회
        info = Info.objects.get(id=data.id)
        info.delete()  # Info 객체 삭제
        return JsonResponse({"message": "Info successfully deleted"}, status=200)
    except Info.DoesNotExist:
        # 해당 ID가 없을 경우 404 응답
        return JsonResponse({"error": "Info with the given id does not exist"}, status=404)
    
# PUT 요청 처리 (정보 수정)
@api3.put("/total/professor/modify", response=InfoCreateSchema)
def modify_info(request, data: InfoUpdateSchema):
    try:
        # `id`에 해당하는 Info 객체 가져오기
        info = Info.objects.get(id=data.id)
    except Info.DoesNotExist:
        return JsonResponse({"error": "Info with the given id does not exist"}, status=404)

    # 수정할 필드들 업데이트
    info.professor = data.professor
    info.college = data.college
    info.department = data.department
    info.description = data.description
    info.photo = data.photo
    info.number = data.number
    info.lab = data.lab
    info.email = data.email
    info.subject1 = data.subject1
    info.subject2 = data.subject2
    info.subject3 = data.subject3

    # 변경 사항 저장
    info.save()

    # 수정된 데이터를 반환
    return InfoCreateSchema.from_orm(info)


# POST 요청 처리 (교수 검색)
@api3.post("/total/professor/search")
def search_professor(request, data: ProfessorSearchSchema):
    professor_name = data.professor
    college_name = data.college
    department_name = data.department  # 요청 본문에서 professor 이름을 가져옴
    page = data.page  # 페이지 번호
    page_size = data.page_size  # 한 페이지에 보여줄 교수 수

    # 검색 조건 동적 생성
    query = Q()
    if professor_name:
        query &= Q(professor__icontains=professor_name)
    if college_name:
        query &= Q(college__icontains=college_name)
    if department_name:
        query &= Q(department__icontains=department_name)

    # 조건에 맞는 데이터를 검색. 조건이 없으면 전체 데이터 반환
    professors = Info.objects.filter(query).order_by('id')

    # 검색된 결과가 없으면 빈 리스트 반환
    if not professors:
        return JsonResponse({"message": "No professors found"}, status=404)
    
    paginator = Paginator(professors, page_size)  # 페이지당 `page_size`개 항목
    page_obj = paginator.get_page(page)

    # 결과 반환
    result = []
    for professor_obj in page_obj:
        result.append({
            "id": professor_obj.id,
            "professor": professor_obj.professor,
            "college": professor_obj.college,
            "department": professor_obj.department,
            "description": professor_obj.description,
            "photo": professor_obj.photo,
            "number": professor_obj.number,
            "lab": professor_obj.lab,
            "email": professor_obj.email,
            "subject1": professor_obj.subject1,
            "subject2": professor_obj.subject2,
            "subject3": professor_obj.subject3,
        })
  # 전체 페이지 수와 항목 수 계산
    total_count = paginator.count  # 전체 데이터 수
    total_pages = paginator.num_pages  # 전체 페이지 수
    

    return JsonResponse({
        "professors": result,
        "page": page,
        "page_size": page_size,
        "total_count": total_count,
        "total_pages": total_pages
        })



@api3.post("/total/lecture/search")
def search_lecture(request, data: SubjectSearchSchema):
    subject_name = data.Subject  # 프론트엔드에서 전달받은 과목명

    # 동적으로 과목별 교수들을 저장할 딕셔너리
    subject_profs = {}

    # 교수 정보가 담긴 테이블을 조회하고 subject1, subject2, subject3에서 과목명 검색
    professors = Info.objects.filter(
        Q(subject1__icontains=subject_name) | 
        Q(subject2__icontains=subject_name) | 
        Q(subject3__icontains=subject_name)
    )

    # 각 교수 정보를 순회하면서 과목별로 교수들 추가
    for professor in professors:
        # subject1에 과목명 포함
        if subject_name in professor.subject1:
            if professor.subject1 not in subject_profs:
                subject_profs[professor.subject1] = []
            subject_profs[professor.subject1].append(professor.professor)

        # subject2에 과목명 포함
        if subject_name in professor.subject2:
            if professor.subject2 not in subject_profs:
                subject_profs[professor.subject2] = []
            subject_profs[professor.subject2].append(professor.professor)

        # subject3에 과목명 포함
        if subject_name in professor.subject3:
            if professor.subject3 not in subject_profs:
                subject_profs[professor.subject3] = []
            subject_profs[professor.subject3].append(professor.professor)

    return subject_profs