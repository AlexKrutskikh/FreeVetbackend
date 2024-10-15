from django.shortcuts import render
from django.shortcuts import redirect
from django.conf import settings
from django.http import HttpResponseRedirect
from rest_framework import generics, status
from rest_framework.response import Response
from .models import Profile
from .serializers import LoginSerializer, SMSVerificationSerializer, RegisterSerializer
from .utils import send_sms
from django.utils import timezone
from datetime import timedelta
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from rest_framework.generics import CreateAPIView


"""Redirect after registration and authorization"""
def custom_login_redirect(request):
    # Получаем URL из сессии или задаем значение по умолчанию
    redirect_url = request.session.get('redirect_url', '/default-url')
    return redirect(redirect_url)


"""Redirect for creating an API for authorization"""

def google_oauth_redirect(request):
    redirect_url = f"{settings.BASE_URL}/users/social-auth/login/google-oauth2/"
    return HttpResponseRedirect(redirect_url)

def facebook_oauth_redirect(request):
    # Используем переменную из settings.py
    redirect_url = f"{settings.BASE_URL}/users/social-auth/login/facebook/"
    return HttpResponseRedirect(redirect_url)






"""Created for testing; it will be removed later"""
def some_view(request):
    return render(request, 'index.html')

def registration_success(request):
    return render(request, 'registration_success.html')

def question_post(request):
    return render(request, 'question.html')


class RegisterView(CreateAPIView):
    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)

        # Проверяем валидность входящих данных
        if serializer.is_valid():
            photo = request.FILES.get('photo', None)
            profile = Profile.objects.create(
                name=serializer.validated_data['name'],
                phone=serializer.validated_data['phone'],
                photo=photo  # Устанавливаем фото, если оно передано
            )
            profile.generate_sms_code()  # Генерация кода
            send_sms(profile.phone, f"Your code is {profile.sms_code}")

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone_number = serializer.validated_data['phone_number']

        try:
            profile = Profile.objects.get(phone=phone_number)
            profile.generate_sms_code()  # Обновляем код при каждом запросе
            send_sms(phone_number, f"Your code is {profile.sms_code}")
            return Response({"message": "Code sent"}, status=status.HTTP_200_OK)
        except Profile.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)


class VerifyCodeView(generics.GenericAPIView):
    serializer_class = SMSVerificationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone_number = serializer.validated_data['phone_number']
        code = serializer.validated_data['code']

        try:
            profile = Profile.objects.get(phone=phone_number, sms_code=code)
            if profile.code_sent_time < timezone.now() - timedelta(seconds=90):
                return Response({"error": "Code expired"}, status=status.HTTP_400_BAD_REQUEST)

            profile.last_login_time = timezone.now()
            profile.save()
            return Response({"message": "Logged in"}, status=status.HTTP_200_OK)
        except Profile.DoesNotExist:
            return Response({"error": "Invalid code"}, status=status.HTTP_400_BAD_REQUEST)

