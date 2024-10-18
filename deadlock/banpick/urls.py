from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # 메인 페이지
    path('room/<str:room_name>/', views.room, name='room'),  # 방 입장 페이지
]