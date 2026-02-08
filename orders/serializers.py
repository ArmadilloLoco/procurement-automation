from rest_framework import serializers
from .models import Order, OrderItem
from products.serializers import ProductSerializer

class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)  # для вывода
    product_id = serializers.IntegerField(write_only=True)  # для создания

    class Meta:
        model = OrderItem
        fields = ('product', 'product_id', 'quantity')

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    client_email = serializers.CharField(source='client.email', read_only=True)

    class Meta:
        model = Order
        fields = ('id', 'client_email', 'delivery_address', 'status', 'created_at', 'items')
        read_only_fields = ('id', 'client_email', 'status', 'created_at')

    def create(self, validated_data):
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