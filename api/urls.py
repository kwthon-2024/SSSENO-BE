from django.urls import path, include

urlpatterns = [
    path('', include('kwopgg.urls')),  # kwopgg.urls를 최상위 URL로 연결
]
