from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from .serializers import RegisterSerializer
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from .models import User
import uuid

@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    """
    Регистрация нового пользователя.
    После успешной регистрации:
    - создаётся токен аутентификации,
    - отправляется приветственное письмо на email.
    """
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        token, _ = Token.objects.get_or_create(user=user)

        # Отправка email-подтверждения регистрации
        send_mail(
            subject="Добро пожаловать!",
            message="Вы успешно зарегистрировались в системе закупок.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=True
        )
        
        return Response({
            'token': token.key,
            'user_id': user.id,
            'email': user.email,
            'is_supplier': user.is_supplier
        }, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def password_reset_request(request):
    """
    Запрос на сброс пароля.
    Генерирует временный токен и отправляет ссылку на email.
    """
    email = request.data.get('email')
    if not email:
        return Response({'error': 'Email обязателен'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response({'detail': 'Если email зарегистрирован, вы получите инструкции.'}, status=status.HTTP_200_OK)

    # Генерация одноразового токена сброса пароля
    token = str(uuid.uuid4())
    user.password_reset_token = token
    user.password_reset_expires = timezone.now() + timedelta(hours=1)
    user.save()

    reset_url = f"http://127.0.0.1:8000/api/auth/password-reset-confirm/?token={token}"

    # Отправка инструкций по email
    send_mail(
        subject="Сброс пароля",
        message=f"Перейдите по ссылке для сброса пароля:\n{reset_url}\n\nСсылка действительна 1 час.",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        fail_silently=True
    )

    return Response({'detail': 'Инструкции отправлены на email'}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def password_reset_confirm(request):
    """
    Подтверждение сброса пароля.
    Принимает токен и новый пароль, проверяет срок действия токена,
    устанавливает новый пароль и очищает токен.
    """
    token = request.data.get('token')
    new_password = request.data.get('new_password')

    if not token or not new_password:
        return Response({'error': 'Токен и новый пароль обязательны'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.get(password_reset_token=token)
    except User.DoesNotExist:
        return Response({'error': 'Неверный или просроченный токен'}, status=status.HTTP_400_BAD_REQUEST)

    # Проверяем срок действия
    if user.password_reset_expires < timezone.now():
        user.password_reset_token = None
        user.password_reset_expires = None
        user.save()
        return Response({'error': 'Токен просрочен'}, status=status.HTTP_400_BAD_REQUEST)

    # Установка нового пароля и очистка токена
    user.set_password(new_password)
    user.password_reset_token = None
    user.password_reset_expires = None
    user.save()

    return Response({'detail': 'Пароль успешно изменён'}, status=status.HTTP_200_OK)