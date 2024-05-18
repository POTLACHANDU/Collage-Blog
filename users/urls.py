from django.urls import path, include
from . import views
from users.views import ChangePasswordView

urlpatterns = [
    path('register/', views.user_register, name='user-register'),
    path('login/', views.user_login, name='user-login'),
    path('logout/', views.user_logout, name='user-logout'),
    path('profile/', views.user_profile, name='user-profile'),
    path('password-change/', ChangePasswordView.as_view(), name='user-passwordchange'),
] 
