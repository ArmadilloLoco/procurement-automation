from django.urls import path
from . import views

urlpatterns = [
    # Создание нового заказа (оформление покупки)
    path('', views.create_order, name='order-create'),
    # Получение списка всех заказов текущего пользователя
    path('my/', views.order_list, name='order-list'),
    # Получение деталей конкретного заказа по ID
    path('<int:pk>/', views.order_detail, name='order-detail'),
]