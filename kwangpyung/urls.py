# from django.urls import path, include

# urlpatterns = [
#     path('', include('kwopgg.urls')),  # '/api/' 경로로 API 연결
#     path('', include('kwsmg.urls')),  # '/api/' 경로로 API 연결
# ]

from django.urls import path, include

urlpatterns = [
    path('kwopgg/', include('kwopgg.urls')),  # 'kwopgg/' 경로로 API 연결
    path('kwsmg/', include('kwsmg.urls')),  # 'kwsmg/' 경로로 API 연결
]
