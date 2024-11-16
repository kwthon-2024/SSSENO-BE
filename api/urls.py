# # 최상위 프로젝트 urls.py
# from django.urls import path, include

# urlpatterns = [
    
#     path('', include('kwsmg.urls')),  # '/api/petitions/' 경로로 kwsmg.urls 연결
#     path('', include('kwopgg.urls')),  # 기존 kwopgg.urls를 최상위 URL로 연결
# ]

from django.urls import path, include

urlpatterns = [
    path('kwsmg/', include('kwsmg.urls')),  # 'kwsmg/' 경로로 kwsmg.urls 연결
    path('kwopgg/', include('kwopgg.urls')),  # 'kwopgg/' 경로로 kwopgg.urls 연결
    path('kwpr/', include('kwpr.urls')),
]
