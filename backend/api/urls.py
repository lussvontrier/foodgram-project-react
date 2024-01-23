from django.urls import path, include
from rest_framework.routers import DefaultRouter

router_v1 = DefaultRouter()

auth_patterns = [
    path('users/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]

v1_patterns = [
    path('', include(router_v1.urls)),
    path('auth/', include(auth_patterns))
]

urlpatterns = [
    path('', include(v1_patterns))
]
