from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import User, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _

"""User model"""

class User(AbstractBaseUser, PermissionsMixin):
    class UserType(models.TextChoices):
        CLIENT = 'CL', _('Client')
        SPECIALIST = 'SP', _('Specialist')

    class RegistrationType(models.TextChoices):
        TWILIO = 'TW', _('Twilio')
        SOCIAL = 'SC', _('Social')

    auth_provider = models.CharField(                                                   # Тип пользователя
        max_length=20,
        choices=RegistrationType.choices,
        default=RegistrationType.SOCIAL,
    )

    registration_time = models.DateTimeField(auto_now_add=True)                         # Время регистрации
    last_login_time = models.DateTimeField(auto_now=True)                               # Время последнего входа
    email = models.EmailField(unique=True, blank=True, null=True)                       # Почта
    USERNAME_FIELD = "email"

    type = models.CharField(                                                            # Тип пользователя
        max_length=20,
        choices=UserType.choices,
        default=UserType.CLIENT,
    )
