from ninja import NinjaAPI, Router
from kwsmg.models import Complaint_form
from kwsmg.schemas import ComplaintFormSchema, PaginatedResponse, ComplaintSearchSchema
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from django.db.models import Q
from datetime import datetime

api2 = NinjaAPI(urls_namespace="kwsmg_api")  # NinjaAPI 객체 생성

# 청원 검색 함수
def search(complaint_title: str = None, description: str = None, accepted: bool = None, search_type: str = None, category: str = None, kw: str = None):
    # 기본적으로 모든 complaint를 가져옵니다.
    complaints = Complaint_form.objects.all().order_by('-created')  # 기본 정렬은 생성일

    # 1. 키워드 검색 (kw가 주어지면 제목, 내용, 중요 항목에서 검색)
    if kw:
        if search_type == 'both':
            complaints = complaints.filter(
                Q(complaint_title__icontains=kw) |
                Q(description__icontains=kw)
            ).distinct()
        elif search_type == 'title':
            complaints = complaints.filter(complaint_title__icontains=kw)  # 제목에서만 검색
        elif search_type == 'description':
            complaints = complaints.filter(description__icontains=kw)  # 내용에서만 검색
    # 2. 제목 검색 (complaint_title가 주어지면 제목에서만 필터링)
    if complaint_title:
        complaints = complaints.filter(complaint_title__icontains=complaint_title)  # 제목에서만 검색

    # 3. 내용 검색 (description이 주어지면 내용에서만 필터링)
    if description:
        complaints = complaints.filter(description__icontains=description)  # 내용에서만 검색

    # 4. 카테고리 필터링 (카테고리가 주어지면 필터링)
    if category:
        complaints = complaints.filter(category__icontains=category)

    # 5. 승인 여부 필터링 (accepted가 주어지면 필터링)
    if accepted is not None:
        complaints = complaints.filter(accepted=accepted)

    return complaints

# 페이지네이션 함수
def paginate(complaints, page: int = 1, per_page: int = 10):
    paginator = Paginator(complaints, per_page)
    page_obj = paginator.get_page(page)
    # 응답할 데이터

    response_data = {
        "total_pages": page_obj.paginator.num_pages,
        "current_page": page_obj.number,
        "total_count": page_obj.paginator.count,
    }
    # 결과가 있다면 results 필드에 데이터를 추가
    if page_obj.object_list:
        response_data["results"] = [
            ComplaintFormSchema.from_orm(complaint) for complaint in page_obj.object_list
        ]

    return response_data

from pydantic import BaseModel

class PageRequestSchema(BaseModel):
    page: int = 1  # 기본 페이지는 1
    per_page: int = 10  # 기본 페이지당 항목은 10개
# 청원 목록 조회 API
    
@api2.post("/petition/complaint/read", response=PaginatedResponse)
def paginate_complaints(request, data: PageRequestSchema):
    page = data.page if data.page else 1  # 페이지가 없으면 1로 기본 설정
    per_page = data.per_page if data.per_page else 10  # per_page가 없으면 10으로 기본 설정
    complaints = Complaint_form.objects.all().order_by('-created')
    # 페이지네이션 처리
    paginated_complaints = paginate(complaints, page, per_page)
    return paginated_complaints

@api2.post("/petition/complaint/search", response=PaginatedResponse)
def search_complaints(request, data: ComplaintSearchSchema):
    complaint_title = data.complaint_title
    description = data.description
    accepted = data.accepted
    search_type = data.search_type
    kw = data.kw
    category = data.category
    # 검색된 청원 목록
    complaints = search(kw=kw, complaint_title=complaint_title, description=description, accepted=accepted, search_type=search_type, category=category)
    # 기본적으로 페이지는 1, 10개씩 반환하도록 설정
    page = data.page if data.page else 1
    # 페이지네이션 처리
    paginated_complaints = paginate(complaints, page)
    return paginated_complaints


class ComplaintSchema(BaseModel):
    complaint_id: int


# 청원 상세 조회 API
@api2.get("/petition/complaint/detail", response=ComplaintFormSchema)
def get_complaint_detail(request, data: ComplaintSchema):
    try:
        # `complaint_id`를 기준으로 데이터를 검색
        complaint = Complaint_form.objects.get(complaint_id=data.complaint_id)
    except Complaint_form.DoesNotExist:
        # 없는 경우 404 에러 반환
        return JsonResponse({"error": "Complaint not found"}, status=404)
    # 검색된 객체를 반환
    return ComplaintFormSchema.from_orm(complaint)


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
    return ComplaintFormSchema.from_orm(new_complaint)


@api2.put("/petition/complaint/modify", response=ComplaintFormSchema)
def update_complaint(request, data: ComplaintFormSchema):
     # complaint_id로 해당 complaint 객체 가져오기
    complaint = get_object_or_404(Complaint_form, complaint_id=data.complaint_id)
    complaint.complaint_title = data.complaint_title
    complaint.description = data.description
    complaint.category = data.category
    complaint.accepted = data.accepted if data.accepted is not None else complaint.accepted
    complaint.gachucount = data.gachucount if data.gachucount is not None else complaint.gachucount
    complaint.answer = data.answer if data.answer is not None else complaint.answer
    # 객체 저장
    complaint.save()
    # 수정된 객체를 응답 형식에 맞게 반환
    return ComplaintFormSchema.from_orm(complaint)

from ninja import Router, Schema
# 응답 스키마 정의
class ComplaintFormsSchema(Schema):
    complaint_id: int
# 응답 스키마 정의
class GachuResponseSchema(Schema):
    안내: str
    청원에_동참한_인원: int
@api2.put("/petition/complaint/gachu", response=GachuResponseSchema)
def gachu_complaint(request, data: ComplaintFormsSchema):
    try:
        # complaint_id를 바탕으로 청원 찾기
        complaint = Complaint_form.objects.get(complaint_id=data.complaint_id)

        # 청원 동의 카운트 증가
        complaint.gachucount += 1
        complaint.save()

        # 성공적인 응답 반환
        return GachuResponseSchema(
            안내="청원에 동의하였습니다.",
            청원에_동참한_인원=complaint.gachucount
        )
    except Complaint_form.DoesNotExist:
        return {"error": "해당 complaint_id를 가진 청원이 존재하지 않습니다."}, 404
    
from ninja import Router, Schema
from pydantic import BaseModel

# 응답 스키마 정의
class DeleteResponseSchema(Schema):
    message: str

# 요청 데이터 스키마 정의
class ComplaintDeleteRequestSchema(BaseModel):
    complaint_id: int

# 청원 삭제 API
@api2.post("/petition/complaint/delete", response=DeleteResponseSchema)
def delete_complaint(request, data: ComplaintDeleteRequestSchema):
    try:
        complaint = Complaint_form.objects.get(complaint_id=data.complaint_id)
        complaint.delete()
        # 성공적인 삭제 후 메시지 반환
        return DeleteResponseSchema(message="청원이 정상적으로 삭제되었습니다.")
    except Complaint_form.DoesNotExist:
        # 청원이 존재하지 않으면 에러 메시지 반환
        return DeleteResponseSchema(message="해당 complaint_id를 가진 청원이 존재하지 않습니다.")

from pydantic import BaseModel

class ComplaintupdateFormSchema(BaseModel):
    complaint_id: int
    answer: str

    class Config:
        orm_mode = True  # ORM 모델을 지원하도록 설정
        from_attributes = True  # from_orm 사용을 위한 설정

# 요청 데이터 및 응답 데이터가 다르기 때문에 응답 형식도 ComplaintupdateFormSchema로 변경
@api2.put("/petition/answer/modify", response=ComplaintupdateFormSchema)
def update_complaint(request, data: ComplaintupdateFormSchema):
    print(data)  # 데이터 확인
    # complaint_id로 해당 complaint 객체 가져오기
    complaint = get_object_or_404(Complaint_form, complaint_id=data.complaint_id)
    complaint.answer = data.answer
    # 객체 저장
    complaint.save()
    # 수정된 객체를 응답 형식에 맞게 반환
    return ComplaintupdateFormSchema.from_orm(complaint)

