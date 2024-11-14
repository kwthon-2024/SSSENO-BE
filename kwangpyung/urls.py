from django.urls import path, include

urlpatterns = [
    path('', include('kwopgg.urls')),  # '/api/' 경로로 API 연결
]
