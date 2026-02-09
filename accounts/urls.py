from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token  

urlpatterns = [
    # Эндпоинт регистрации нового пользователя
    path('register/', views.register, name='register'),
    # Стандартный DRF эндпоинт для получения токена по логину/паролю
    path('login/', obtain_auth_token, name='login'),
    # Запрос на сброс пароля (отправка токена на email)
    path('password-reset/', views.password_reset_request, name='password-reset'),
    # Подтверждение сброса пароля и установка нового пароля
    path('password-reset-confirm/', views.password_reset_confirm, name='password-reset-confirm'),
]