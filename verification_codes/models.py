from django.db import models
from django.utils import timezone
import random

class VerifyCcode(models.Model):

    verify_code = models.CharField(max_length=6, blank=True, null=True)
    is_used = models.BooleanField(default=False)

class SmsCode(models.Model):

    sms_code = models.CharField(max_length=6, blank=True, null=True)
    code_sent_time = models.DateTimeField(blank=True, null=True)
    phone = models.CharField(max_length=50, unique=True, blank=True, null=True)


    def generate_sms_code(self):
        self.sms_code = str(random.randint(100000, 999999))
        self.code_sent_time = timezone.now()
        self.save()

    def __str__(self):
        return self.name