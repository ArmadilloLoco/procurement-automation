from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid

class User(AbstractUser):
    """
    Расширенная модель пользователя с поддержкой ролей:
    - обычный клиент (is_supplier=False)
    - поставщик (is_supplier=True)
    
    Также содержит поля для механизма сброса пароля.
    """
    email = models.EmailField(unique=True)
    is_supplier = models.BooleanField(default=False)
    
    # Поля для восстановления пароля через email
    password_reset_token = models.CharField(max_length=100, blank=True, null=True)
    password_reset_expires = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.email