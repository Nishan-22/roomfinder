from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [

    # ROOMS
    path('', views.room_list, name='room_list'),
    path('<int:id>/', views.room_detail, name='room_detail'),
    path('add/', views.add_room, name='add_room'),
    path('edit/<int:id>/', views.edit_room, name='edit_room'),
    path('delete/<int:id>/', views.delete_room, name='delete_room'),

    # AUTH
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='auth/login.html'), name='login'),

    # CUSTOM LOGOUT WITH CONFIRMATION PAGE
    path('logout/', views.logout_confirm, name='logout'),
]
