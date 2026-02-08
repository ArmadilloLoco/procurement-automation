from django.urls import path
from . import views

urlpatterns = [
    path('', views.create_order, name='order-create'),
    path('my/', views.order_list, name='order-list'),
    path('<int:pk>/', views.order_detail, name='order-detail'),
]