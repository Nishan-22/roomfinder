from django.urls import path
from . import views

urlpatterns = [
    path('', views.room_list, name='room_list'),
    path('<int:id>/', views.room_detail, name='room_detail'),
    path('add/', views.add_room, name='add_room'),
    path('edit/<int:id>/', views.edit_room, name='edit_room'),
    path('delete/<int:id>/', views.delete_room, name='delete_room'),


]
