# backend/urls.py
from django.urls import path
from backend.views import user_registration_view, user_list, user_detail, user_login_view, user_logout_view

urlpatterns = [
    path('users/register/', user_registration_view, name='user-register'),
    path('users/', user_list, name='user-list'),
    path('users/<int:pk>/', user_detail, name='user-detail'),
    path('login/', user_login_view, name='user-login'),
    path('logout/', user_logout_view, name='user-logout'),
]
