from django.db import models
from django.utils import timezone
import random



"""User model"""


class Profile(models.Model):
    photo = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    auth_provider = models.CharField(max_length=50, default='Twilio')                   # Социальная сеть
    name = models.CharField(max_length=50)                                              # Имя
    registration_time = models.DateTimeField(auto_now_add=True)                         # Время регистрации
    last_login_time = models.DateTimeField(auto_now=True)                               # Время последнего входа
    is_user = models.BooleanField(default=False)                                        # Роль
    is_active = models.BooleanField(default=False)                                      # Состояние аккаунта
    last_name = models.CharField(max_length=30, blank=True, null=True)                  # Фамилия
    phone = models.CharField(max_length=50, unique=True)                                # Номер телефона
    email = models.EmailField(unique=True, blank=True, null=True)                       # Почта

# Новые поля для SMS-кода
    sms_code = models.CharField(max_length=6, blank=True, null=True)
    code_sent_time = models.DateTimeField(blank=True, null=True)

    def generate_sms_code(self):
        self.sms_code = str(random.randint(100000, 999999))
        self.code_sent_time = timezone.now()
        self.save()

    def __str__(self):
        return self.name
