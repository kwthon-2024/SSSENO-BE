from django.views.decorators.csrf import csrf_exempt
from ninja import NinjaAPI
from .models import classroom_inf, classroom_review
from .schemas import *
from typing import List
from django.http import JsonResponse
from django.db.models import Q
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404


api = NinjaAPI()

#구현완료
@csrf_exempt
@api.post('/classroom/room/search', response=List[dict])
def search(request, data: SearchRequestSchema):
    try:
        building_title = data.building_title
        capacity_max = data.capacity_max 

        all_classrooms = classroom_inf.objects.all()
        result_data = []

        for classroom in all_classrooms:
            if classroom.building_name == building_title and classroom.capacity >= capacity_max:
                result_data.append({
                    "building_name": classroom.building_name,
                    "capacity": classroom.capacity,
                    "place_name": classroom.place_name,
                })

        if result_data:
            return JsonResponse({"data": result_data}, status=200)
        else:
            return JsonResponse({"message": "해당 조건에 맞는 강의실이 없습니다."}, status=404)

    except Exception as e:

        print(f"Error: {str(e)}")
        return JsonResponse({"message": "서버에서 오류가 발생했습니다."}, status=500)
    
@csrf_exempt
@api.post('/classroom/room/filter', response=List[dict])
def search(request, data: SearchfilterRequestSchema):
    try:
        # 요청 데이터에서 필터 값들 추출
        building_title = data.building_title
        capacity_max = data.capacity_max
        type = data.type
        has_projector = data.has_projector
        has_mic = data.has_mic
        desk_type = data.desk_type

        # 모든 강의실 데이터를 가져오기
        all_classrooms = classroom_inf.objects.all()

        result = []

        # 필터 조건들을 하나의 리스트로 저장
        filters = [
            (building_title, lambda c: c.building_name == building_title),
            (capacity_max, lambda c: c.capacity <= capacity_max if capacity_max is not None else True),
            (type, lambda c: c.type == type if type is not None else True),
            (has_projector, lambda c: c.has_projector == has_projector if has_projector is not None else True),
            (has_mic, lambda c: c.has_mic == has_mic if has_mic is not None else True),
            (desk_type, lambda c: c.desk_type == desk_type if desk_type is not None else True),
        ]

        # 모든 강의실을 순회하며 필터링
        for classroom in all_classrooms:
            # 각 필터 조건을 체크
            if all(condition(classroom) if value else True for value, condition in filters):
                # 조건에 맞는 강의실을 결과 리스트에 추가
                result.append({
                    "Building_title": classroom.building_name,
                    "Place_title": classroom.place_name,
                    "Type": classroom.type,
                    "Has_projector": classroom.has_projector,
                    "Has_mic": classroom.has_mic,
                    "Desk_type": classroom.desk_type
                })

        # 결과가 있으면 반환
        if result:
            return JsonResponse({"success": True, "data": result}, status=200)
        else:
            # 결과가 없으면 오류 메시지 반환
            return JsonResponse({"message": "조건에 맞는 강의실이 없습니다."}, status=404)

    except Exception as e:
        # 예외 발생 시 오류 메시지 출력
        print(f"Error: {str(e)}")
        return JsonResponse({"message": "서버에서 오류가 발생했습니다."}, status=500)



    
#구현완료
@csrf_exempt
@api.post('/classroom/room/list', response=ClassroomListResponse)
def search(request, page: int = 1):
    classrooms = classroom_inf.objects.all()


    paginator = Paginator(classrooms, 10)
    current_page = paginator.page(page)


    classrooms_data = [
        ClassroomSchema(
            Building_title=classroom.building_name,
            Place_title=classroom.place_name,
            capacity=classroom.capacity,
            rating=classroom.rating
        )
        for classroom in current_page.object_list
    ]


    pagination_info = PaginationInfo(
        current_page=current_page.number,
        per_page=paginator.per_page,
        total_items=paginator.count,
        total_pages=paginator.num_pages
    )


    return JsonResponse({
        "success": True,
        "data": {
            "classrooms": [classroom.dict() for classroom in classrooms_data],  
            "pagination": pagination_info.dict()
        }
    })

#구현완료
@csrf_exempt
@api.post("/classroom/room/detail", response=List[ClassroomDetailResponseSchema])
def classroom_detail(request, data: ClassroomDetailRequestSchema):
    try:
        print(f"Request Data: {data}")

        classrooms = classroom_inf.objects.all()

        filtered_classrooms = [
            classroom for classroom in classrooms
            if classroom.building_name == data.building_name and classroom.place_name == data.place_name
        ]

        if filtered_classrooms:
            result = [
                ClassroomDetailResponseSchema(
                    building_name=classroom.building_name,
                    place_name=classroom.place_name,
                    capacity=classroom.capacity,
                    rating=classroom.rating
                )
                for classroom in filtered_classrooms
            ]
            return result
        else:
            return JsonResponse({"message": "조건에 맞는 강의실이 없습니다."}, status=404)
    
    except Exception as e:
        print(f"Error: {str(e)}")
        return JsonResponse({"message": "서버에서 오류가 발생했습니다."}, status=500)


#구현완료 - models.py 수정해야함.
@api.post("/classroom/room/create", response=ClassroomCreateResponseSchema)
def create_classroom(request, data: ClassroomCreateRequestSchema):

    classroom = classroom_inf.objects.create(
        image_id=data.image_id,
        building_name=data.building_name,
        capacity=data.capacity_min,
        place_name=data.place_name,
        rating=data.rating,
        description=data.description,
        type=data.type,
        has_projector=data.has_projector,
        has_mic=data.has_mic,
        desk_type=data.desk_type,
        reserved_time=data.reserved_time,
        reserved=data.reserved
    )


    return {
        "success": True,
        "message": "강의실 정보가 성공적으로 저장되었습니다.",
        "data": {
            "image_id": classroom.image_id,
            "building_name": classroom.building_name,
            "capacity_min": classroom.capacity,
            "place_name": classroom.place_name,
            "rating": classroom.rating,
            "description": classroom.description,
            "filter": {
                "type": classroom.type,
                "has_projector": classroom.has_projector,
                "has_mic": classroom.has_mic,
                "desk_type": classroom.desk_type,
            }
        }
    }

#구현완료
@api.post("/classroom/room/update", response=ClassroomCreateResponseSchema)
def update_classroom(request, data: ClassroomCreateRequestSchema):
    try:
        classrooms = classroom_inf.objects.filter(building_name=data.building_name, place_name=data.place_name)

        if classrooms.count() > 1:
            return JsonResponse({"message": "조건에 맞는 강의실이 여러 개 존재합니다."}, status=400)

        if not classrooms.exists():
            return JsonResponse({"message": "강의실이 존재하지 않습니다."}, status=404)

        classroom = classrooms.first()

        classroom.image_id = data.image_id
        classroom.building_name = data.building_name
        classroom.capacity = data.capacity_min
        classroom.place_name = data.place_name
        classroom.rating = data.rating
        classroom.description = data.description
        classroom.type = data.type
        classroom.has_projector = data.has_projector
        classroom.has_mic = data.has_mic
        classroom.desk_type = data.desk_type
        classroom.reserved_time = data.reserved_time
        classroom.reserved = data.reserved


        classroom.save()


        return {
            "success": True,
            "message": "강의실 정보가 성공적으로 업데이트되었습니다.",
            "data": {
                "image_id": classroom.image_id,
                "building_name": classroom.building_name,
                "capacity_min": classroom.capacity,
                "place_name": classroom.place_name,
                "rating": classroom.rating,
                "description": classroom.description,
                "filter": {
                    "type": classroom.type,
                    "has_projector": classroom.has_projector,
                    "has_mic": classroom.has_mic,
                    "desk_type": classroom.desk_type,
                }
            }
        }
    
    except classroom_inf.DoesNotExist:
        return JsonResponse({"message": "강의실이 존재하지 않습니다."}, status=404)
    except Exception as e:
        return JsonResponse({"message": f"서버에서 오류가 발생했습니다: {str(e)}"}, status=500)

#구현완료
@api.post("/classroom/room/delete", response=ClassroomDeleteResponseSchema)
def delete_classroom(request, data: ClassroomDeleteRequestSchema):

    classroom = get_object_or_404(classroom_inf, building_name=data.building_name, place_name=data.place_name)


    classroom.delete()


    return {
        "success": True,
        "message": "강의실 정보가 성공적으로 삭제되었습니다."
    }

#구현완료
@api.post("/classroom/room/detail-page", response=ClassroomMoreDetailResponseSchema)
def classroom_detail(request, data: ClassroomMoreDetailRequestSchema):
    try:
        
        classrooms = classroom_inf.objects.filter(building_name=data.building_name, place_name=data.place_name)


        if not classrooms.exists():
            return JsonResponse({"message": "조건에 맞는 강의실이 존재하지 않습니다."}, status=404)

        classroom = classrooms.first()


        response_data = {
            "image_id": f"/image/{classroom.building_name}{classroom.place_name}",
            "building_name": classroom.building_name,
            "capacity": classroom.capacity,
            "place_name": classroom.place_name,
            "rating": classroom.rating,
            "description": classroom.description,
            "type": classroom.type,
            "has_projector": classroom.has_projector,
            "has_mic": classroom.has_mic,
            "desk_type": classroom.desk_type,
            "reserved": classroom.reserved
        }

        return JsonResponse({
            "success": True,
            "data": response_data
        })

    except Exception as e:
        # 예외 처리
        return JsonResponse({"message": f"서버에서 오류가 발생했습니다: {str(e)}"}, status=500)
