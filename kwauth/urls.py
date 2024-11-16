from django.urls import path
from .api import api4  

urlpatterns = [
    path("api/", api4.urls),  # NinjaAPI에 정의된 모든 경로를 'api/'로 시작하게 설정
]
