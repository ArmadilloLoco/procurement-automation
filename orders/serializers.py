from rest_framework import serializers
from .models import Order, OrderItem
from products.serializers import ProductSerializer

class OrderItemSerializer(serializers.ModelSerializer):
    """
    Сериализатор элемента заказа.
    Использует два поля для гибкости:
    - product_id (write_only) - для создания заказа (клиент передаёт ID),
    - product (read_only) - для отображения полной информации о товаре в ответе.
    """    
    product = ProductSerializer(read_only=True)  # для вывода полной информации о товаре
    product_id = serializers.IntegerField(write_only=True)  # для создания: клиент передаёт ID

    class Meta:
        model = OrderItem
        fields = ('product', 'product_id', 'quantity')

class OrderSerializer(serializers.ModelSerializer):
    """
    Основной сериализатор заказа.
    Автоматически привязывает заказ к текущему пользователю (client).
    Включает вложенные элементы заказа с полной информацией о товарах.
    """    
    items = OrderItemSerializer(many=True)
    client_email = serializers.CharField(source='client.email', read_only=True)

    class Meta:
        model = Order
        fields = ('id', 'client_email', 'delivery_address', 'status', 'created_at', 'items')
        read_only_fields = ('id', 'client_email', 'status', 'created_at')

    def create(self, validated_data):
        """
        Создание заказа и связанных элементов.
        Клиент берётся из контекста запроса (авторизованный пользователь).
        """
        items_data = validated_data.pop('items')
        user = self.context['request'].user
        order = Order.objects.create(client=user, **validated_data)

        for item in items_data:
            OrderItem.objects.create(
                order=order,
                product_id=item['product_id'],
                quantity=item['quantity']
            )
        return order