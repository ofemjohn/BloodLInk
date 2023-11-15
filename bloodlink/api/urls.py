# backend/urls.py
from django.urls import path
from backend.views import user_registration_view, user_list, user_detail

urlpatterns = [
    path('users/register/', user_registration_view, name='user-register'),
    path('users/', user_list, name='user-list'),
    path('users/<int:pk>/', user_detail, name='user-detail'),
]
