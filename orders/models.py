from django.db import models
from accounts.models import User
from products.models import Product

class Order(models.Model):
    """
    Модель заказа.
    Связана с клиентом (User), содержит адрес доставки, статус и дату создания.
    Статус позволяет отслеживать этапы обработки заказа в системе.
    """    
    STATUS_CHOICES = [
        ('pending', 'Ожидает подтверждения'),
        ('confirmed', 'Подтверждён'),
        ('shipped', 'Отправлен'),
        ('delivered', 'Доставлен'),
    ]
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    delivery_address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"Заказ #{self.id} от {self.client.email}"

class OrderItem(models.Model):
    """
    Промежуточная модель для связи заказа и товаров.
    Позволяет одному заказу содержать несколько товаров в заданном количестве.
    Поддерживает товары от разных поставщиков в одном заказе — требование ТЗ.
    """    
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"