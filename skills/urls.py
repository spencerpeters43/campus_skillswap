from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('skills/<int:pk>/', views.skill_detail, name='skill_detail'),
    path('skills/new/', views.create_post, name='create_post'),
    path('skills/<int:pk>/edit/', views.edit_post, name='edit_post'),
    path('skills/<int:pk>/delete/', views.delete_post, name='delete_post'),
    path('skills/<int:pk>/review/', views.add_review, name='add_review'),
    path('register/', views.register, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
]
