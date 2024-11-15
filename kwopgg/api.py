from django.views.decorators.csrf import csrf_exempt
from ninja import NinjaAPI
from .models import ClassroomInfDev, ClassroomReviewDev
from .schemas import *
from typing import List
from django.http import JsonResponse
from django.db.models import Q
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404


api = NinjaAPI(urls_namespace="kwopgg_api")

#구현완료
@csrf_exempt
@api.post('/classroom/room/search', response=List[dict])
def search(request, data: SearchRequestSchema):
    try:
        building_title = data.building_title
        capacity_max = data.capacity_max 

        all_classrooms = ClassroomInfDev.objects.all()
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
    
#구현완료
@csrf_exempt
@api.post('/classroom/room/filter', response=List[dict])
def search(request, data: SearchfilterRequestSchema):
    try:
        building_title = data.building_title
        capacity_max = data.capacity_max
        type = data.type
        has_projector = data.has_projector
        has_mic = data.has_mic
        desk_type = data.desk_type

        all_classrooms = ClassroomInfDev.objects.all()

        result = []


        filters = [
            (building_title, lambda c: c.building_name == building_title),
            (capacity_max, lambda c: c.capacity <= capacity_max if capacity_max is not None else True),
            (type, lambda c: c.type == type if type is not None else True),
            (has_projector, lambda c: c.has_projector == has_projector if has_projector is not None else True),
            (has_mic, lambda c: c.has_mic == has_mic if has_mic is not None else True),
            (desk_type, lambda c: c.desk_type == desk_type if desk_type is not None else True),
        ]

        for classroom in all_classrooms:
            if all(condition(classroom) if value else True for value, condition in filters):
                result.append({
                    "Building_title": classroom.building_name,
                    "Place_title": classroom.place_name,
                    "Type": classroom.type,
                    "Has_projector": classroom.has_projector,
                    "Has_mic": classroom.has_mic,
                    "Desk_type": classroom.desk_type
                })


        if result:
            return JsonResponse({"success": True, "data": result}, status=200)
        else:
            return JsonResponse({"message": "조건에 맞는 강의실이 없습니다."}, status=404)

    except Exception as e:

        print(f"Error: {str(e)}")
        return JsonResponse({"message": "서버에서 오류가 발생했습니다."}, status=500)



    
#구현완료
@csrf_exempt
@api.post('/classroom/room/list', response=ClassroomListResponse)
def search(request, page: int = 1):
    classrooms = ClassroomInfDev.objects.all()


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

        classrooms = ClassroomInfDev.objects.all()

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

    classroom = ClassroomInfDev.objects.create(
        image_id=data.image_id,
        building_name=data.building_name,
        capacity=data.capacity_min,
        place_name=data.place_name,
        rating=data.rating,
        description=data.description,
        type=data.type,
        has_projector=data.has_projector,
        has_mic=data.has_mic,
        desk_type=data.desk_type
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
        classrooms = ClassroomInfDev.objects.filter(building_name=data.building_name, place_name=data.place_name)

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
    
    except ClassroomInfDev.DoesNotExist:
        return JsonResponse({"message": "강의실이 존재하지 않습니다."}, status=404)
    except Exception as e:
        return JsonResponse({"message": f"서버에서 오류가 발생했습니다: {str(e)}"}, status=500)

#구현완료
@api.post("/classroom/room/delete", response=ClassroomDeleteResponseSchema)
def delete_classroom(request, data: ClassroomDeleteRequestSchema):

    classroom = get_object_or_404(ClassroomInfDev, building_name=data.building_name, place_name=data.place_name)


    classroom.delete()


    return {
        "success": True,
        "message": "강의실 정보가 성공적으로 삭제되었습니다."
    }

#구현완료
@api.post("/classroom/room/detail-page", response=ClassroomMoreDetailResponseSchema)
def classroom_detail(request, data: ClassroomMoreDetailRequestSchema):
    try:
        
        classrooms = ClassroomInfDev.objects.filter(building_name=data.building_name, place_name=data.place_name)


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

#구현완료
@api.post("/classroom/room/review", response=ClassroomReviewResponseSchema)
def review_room(request, data: ClassroomReviewRequestSchema):

    classroom = get_object_or_404(ClassroomReviewDev, building_name=data.building_name, place_name=data.place_name)

    print(classroom)
    return {
        "success": True,
        "message": "강의실 리뷰가 성공적으로 조회되었습니다.",
        "building_name": classroom.building_name,
        "place_name": classroom.place_name,
        "mic_status": classroom.mic_status,
        "clean_status": classroom.clean_status,
        "size_satisfaction": classroom.size_satisfaction,
        "air_conditioner_status": classroom.air_conditioner_status,
        "user_id": classroom.user_id,
    }

#구현완료
@api.post("/classroom/room/review/create", response=ClassroomReviewCreateResponseSchema)
def create_review(request, data: ClassroomReviewCreateRequestSchema):

    review = ClassroomReviewDev.objects.create(
        building_name=data.building_name,
        place_name=data.place_name,
        mic_status=data.mic_status,
        clean_status=data.clean_status,  
        size_satisfaction=data.size_satisfaction,
        air_conditioner_status=data.air_conditioner_status,
        user_id=data.user_id,
    )

    return {
        "success": True,
        "message": "강의실 리뷰가 등록되었습니다.",
        "building_name": review.building_name,
        "place_name": review.place_name,
        "mic_status": review.mic_status,
        "clean_status": review.clean_status,  # 응답에 맞춰 cleanliness로 반환
        "size_satisfaction": review.size_satisfaction,
        "air_conditioner_status": review.air_conditioner_status,
        "user_id": review.user_id,
    }

#구현완료
@api.put("/classroom/room/review/update", response=ClassroomReviewUpdateResponseSchema)
def update_review(request, data: ClassroomReviewUpdateRequestSchema):

    review = get_object_or_404(ClassroomReviewDev, building_name=data.building_name, place_name=data.place_name)

    review.mic_status = data.mic_status
    review.clean_status = data.cleanliness  
    review.size_satisfaction = data.size_satisfaction
    review.air_conditioner_status = data.air_conditioner_status
    review.user_id = data.user_id
    
    review.save()

    return {
        "success": True,
        "message": "강의실 리뷰가 성공적으로 업데이트되었습니다.",
        "building_name": review.building_name,
        "place_name": review.place_name,
        "mic_status": review.mic_status,
        "cleanliness": review.clean_status,
        "size_satisfaction": review.size_satisfaction,
        "air_conditioner_status": review.air_conditioner_status,
        "user_id": review.user_id,
    }

