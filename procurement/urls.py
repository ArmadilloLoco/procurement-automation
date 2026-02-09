"""
URL configuration for procurement project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
"""
URL configuration for procurement project.

Архитектура API:
- /api/auth/ — регистрация, вход, восстановление пароля.
- /api/products/ — каталог товаров и детали.
- /api/orders/ — оформление и просмотр заказов.
- Корень (/) возвращает справку по API (удобно для отладки).
"""
from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse

def index(request):
    """
    Корневой эндпоинт — возвращает справку по доступным API.
    Упрощает навигацию при разработке и тестировании.
    """
    return JsonResponse({
        'message': 'Welcome to Procurement Automation API',
        'endpoints': {
            'admin': '/admin/',
            'auth': '/api/auth/',
            'products': '/api/products/',
            'orders': '/api/orders/',
        }
    })

urlpatterns = [
    path('', index),                      # Справка по API
    path('admin/', admin.site.urls),      # Админка Django (для управления данными)
    path('api/auth/', include('accounts.urls')),    # Аутентификация
    path('api/products/', include('products.urls')), # Товары
    path('api/orders/', include('orders.urls')),     # Заказы
]