from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.core.mail import send_mail
from django.conf import settings
from .models import Order
from .serializers import OrderSerializer

def send_order_confirmation(order):
    """
    Отправка email-подтверждения клиенту после оформления заказа.
    Реализует требование: «отправка заказа на email клиента».
    """    
    subject = f"Ваш заказ #{order.id} принят"
    body = f"Спасибо за заказ!\nАдрес доставки: {order.delivery_address}\nСтатус: {order.get_status_display()}"
    send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [order.client.email])

def send_admin_invoice(order):
    """
    Отправка накладной администратору (или логисту).
    Формирует список товаров с указанием поставщика — важно для закупок.
    Реализует требование: «отправка накладной на email администратора».
    """    
    items = "\n".join([
        f"- {item.product.name} x{item.quantity} ({item.product.supplier.company_name})"
        for item in order.items.all()
    ])
    subject = f"Новый заказ #{order.id}"
    body = f"Клиент: {order.client.email}\nАдрес: {order.delivery_address}\nТовары:\n{items}"
    send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [settings.ADMIN_EMAIL])

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_order(request):
    """
    Эндпоинт оформления заказа.
    Требования:
    - Только клиенты могут делать заказы (поставщики - нет).
    - Заказ может содержать товары от нескольких поставщиков.
    - После создания отправляются два email: клиенту и админу.
    """    
    if request.user.is_supplier:
        return Response({'error': 'Поставщики не могут делать заказы'}, status=status.HTTP_403_FORBIDDEN)

    serializer = OrderSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        order = serializer.save()
        send_order_confirmation(order)
        send_admin_invoice(order)

        response_serializer = OrderSerializer(order, context={'request': request})
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def order_list(request):
    """
    Получение списка всех заказов текущего пользователя.
    Использует prefetch_related для оптимизации запросов к БД.
    """    
    orders = Order.objects.filter(client=request.user).prefetch_related('items__product__supplier')
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def order_detail(request, pk):
    """
    Получение деталей конкретного заказа.
    Доступ только к своим заказам (защита через фильтр по client=request.user).
    """    
    try:
        order = Order.objects.prefetch_related('items__product__supplier').get(id=pk, client=request.user)
    except Order.DoesNotExist:
        return Response({'error': 'Заказ не найден'}, status=status.HTTP_404_NOT_FOUND)
    serializer = OrderSerializer(order)
    return Response(serializer.data)