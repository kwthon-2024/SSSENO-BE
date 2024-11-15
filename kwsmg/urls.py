# kwsmg/urls.py
from django.urls import path
from .views import api2  # views에서 정의한 api 객체 가져오기

urlpatterns = [
    path('api/', api2.urls),  # /api/petitions/ 경로로 연결
]
