from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
import random

"""User model"""

class Profile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)  # Связь с моделью User
    auth_provider = models.CharField(max_length=50, default='Twilio')                   # Социальная сеть
    name = models.CharField(max_length=50)                                              # Имя
    registration_time = models.DateTimeField(auto_now_add=True)                         # Время регистрации
    last_login_time = models.DateTimeField(auto_now=True)                               # Время последнего входа
    is_user = models.BooleanField(default=False)                                        # Роль
    is_active = models.BooleanField(default=False)                                      # Состояние аккаунта
    last_name = models.CharField(max_length=30, blank=True, null=True)                  # Фамилия
    phone = models.CharField(max_length=50, unique=True)                                # Номер телефона
    email = models.EmailField(unique=True, blank=True, null=True)                       # Почта
    sms_code = models.CharField(max_length=6, blank=True, null=True)                    # Код SMS
    code_sent_time = models.DateTimeField(blank=True, null=True)                        # Время отправки кода
    image = models.ImageField(upload_to='profile_images/', blank=True, null=True)       # Поле для хранения изображения профиля

    def generate_sms_code(self):
        self.sms_code = str(random.randint(100000, 999999))  # Генерация SMS-кода
        self.code_sent_time = timezone.now()  # Время отправки кода
        self.save()  # Сохранение изменений в базе данных

    def __str__(self):
        return self.name  # Представление профиля по имени
