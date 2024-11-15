from ninja import NinjaAPI, Router
from kwsmg.models import Complaint_form
from kwsmg.schemas import ComplaintFormSchema, PaginatedResponse
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from django.db.models import Q
from datetime import datetime

api2 = NinjaAPI(urls_namespace="kwsmg_api")  # NinjaAPI 객체 생성

# 청원 검색 함수
def search(query: str = None, accepted: bool = None, search_type: str = 'both', category: str = None, complaint_title: str = None):
    # 기본적으로 모든 complaint를 가져옵니다.
    complaints = Complaint_form.objects.all().order_by('-created')
    # 1. 카테고리 필터링 (카테고리가 주어지면 필터링)
    if category:
        complaints = complaints.filter(category__icontains=category)
    # 2. 승인 여부 필터링 (accepted가 주어지면 필터링)
    if accepted is None:
        complaints = complaints.filter(accepted=accepted)
    # 3. 제목/내용 검색 (query와 search_type이 주어지면 필터링)
    if complaint_title:
        complaints = complaints.filter(complaint_title__icontains=complaint_title)  # 제목에서만 검색
    if query:
        if search_type == 'both':
            complaints = complaints.filter(
                Q(complaint_title__icontains=query) |
                Q(description__icontains=query)
            ).distinct()  # 제목이나 내용에 쿼리 값이 포함된 데이터를 검색
        elif search_type == 'title':
            complaints = complaints.filter(complaint_title__icontains=query)  # 제목에서만 검색
        elif search_type == 'description':
            complaints = complaints.filter(description__icontains=query)  # 내용에서만 검색
    return complaints

# 페이지네이션 함수
def paginate(complaints, page: int = 1, per_page: int = 10):
    paginator = Paginator(complaints, per_page)
    page_obj = paginator.get_page(page)
    return PaginatedResponse(
        total_pages=page_obj.paginator.num_pages,
        current_page=page_obj.number,
        total_count=page_obj.paginator.count,
        results=[ComplaintFormSchema.from_orm(complaint) for complaint in page_obj.object_list]
        # ORM 객체를 Pydantic 모델로 변환
    )

# 청원 목록 조회 API
@api2.get("/petition/complaint/read", response=PaginatedResponse)
def read_complaints(request, accepted: bool = False, search_type: str = 'both', query: str = '', category: str = '',
                    page: int = 1):
    # 검색 조건에 맞는 불만 사항 조회
    complaints = search(query=query, accepted=accepted, search_type=search_type, category=category)
    # 페이지네이션 처리
    paginated_complaints = paginate(complaints, page)
    # 결과 데이터를 PaginatedResponse 형식으로 반환
    return paginated_complaints

# 청원 상세 조회 API
@api2.get("/petition/complaint/detail/{pk}", response=ComplaintFormSchema)
def read_complaints_detail(request, pk: int):
    complaint_entity = get_object_or_404(Complaint_form, complaint_id=pk)  # complaint_id로 조회
    result = ComplaintFormSchema.from_orm(complaint_entity)  # ORM 객체를 Pydantic 모델로 변환
    return result


# 청원 생성 API 비상 1번
from datetime import datetime

@api2.post("/petition/complaint/add", response=ComplaintFormSchema)
def create_complaint(request, data: ComplaintFormSchema):
    # 새로운 청원 생성
    new_complaint = Complaint_form.objects.create(
        complaint_id=data.complaint_id,
        complaint_title=data.complaint_title,
        description=data.description,
        accepted=data.accepted,
        gachucount=data.gachucount,
        category=data.category,
        answer=data.answer,
        created=data.created if data.created else datetime.now(),  # created 값이 없으면 현재 시간 사용
    )
    return new_complaint


@api2.put("/petition/complaint/modify/{pk}", response=ComplaintFormSchema)
def update_complaint(request, pk: int, data: ComplaintFormSchema):
    print("수정할 데이터", data)

    # pk를 기반으로 Complaint_form 객체 가져오기
    complaint = get_object_or_404(Complaint_form, complaint_id=pk)

    # 받은 데이터로 필드 업데이트
    complaint.complaint_title = data.complaint_title
    complaint.description = data.description
    complaint.category = data.category
    complaint.accepted = data.accepted if data.accepted is not None else complaint.accepted
    complaint.gachucount = data.gachucount if data.gachucount is not None else complaint.gachucount
    complaint.answer = data.answer if data.answer is not None else complaint.answer
    complaint.created = data.created if data.created else complaint.created  # created 값이 없으면 기존 값 유지

    # 객체 저장
    complaint.save()

    # 수동으로 반환할 데이터 구성
    return {
        "complaint_id": complaint.complaint_id,
        "complaint_title": complaint.complaint_title,
        "description": complaint.description,
        "accepted": complaint.accepted,
        "gachucount": complaint.gachucount,
        "category": complaint.category,
        "answer": complaint.answer,
        "created": complaint.created
    }


# 청원 삭제 API
@api2.delete("/petition/complaint/{pk}")
def delete_complaint(request, pk: int):
    complaint = get_object_or_404(Complaint_form, complaint_id=pk)
    complaint.delete()
    return {"message": "청원이 정상적으로 삭제되었습니다."}

# 청원 동의 API
@api2.put("/petition/complaint/gachu/{pk}")
def recommend_complaint(request, pk: int):
    complaint = get_object_or_404(Complaint_form, complaint_id=pk)
    complaint.gachucount += 1
    complaint.save()
    return {
        "안내": "청원에 동의하였습니다.",
        "청원에 동참한 인원": complaint.gachucount
    }


# 청원 답변 입력 API (특정 사용자만 가능)
@api2.put("/petition/answer/modify/{complaint_id}", response=ComplaintFormSchema)
def add_answer(request, pk: int, data: ComplaintFormSchema):
    print("수정할 데이터", data)
    # pk를 기반으로 Complaint_form 객체 가져오기
    complaint = get_object_or_404(Complaint_form, complaint_id=pk)
    # 받은 데이터로 필드 업데이트
    complaint.answer = data.answer
    complaint.save()
    return ComplaintFormSchema.from_attributes(complaint)  # 수정된 객체를 Pydantic 모델로 변환하여 반환




# # 청원 답변 조회 API
# @router.get("/petition/answer/read/{complaint_id}", response=ComplaintFormSchema)
# def get_complaint_answer(request, complaint_id: int):
#     complaint = get_object_or_404(Complaint_form, complaint_id=complaint_id)
#     # 답변이 있을 경우에만 포함
#     return ComplaintFormSchema.from_orm(complaint)
