from django.urls import path
from .api import api3  

urlpatterns = [
    path("api/", api3.urls),  # NinjaAPI에 정의된 모든 경로를 'api/'로 시작하게 설정
]
