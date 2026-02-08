from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token  

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', obtain_auth_token, name='login'),
    path('password-reset/', views.password_reset_request, name='password-reset'),
    path('password-reset-confirm/', views.password_reset_confirm, name='password-reset-confirm'),
]