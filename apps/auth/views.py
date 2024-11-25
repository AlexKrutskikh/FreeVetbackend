from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.conf import settings
from django.http import HttpResponseRedirect, JsonResponse
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.utils import timezone
from datetime import timedelta
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from twilio.base.exceptions import TwilioRestException
from django.shortcuts import render

from apps.profiles.models import Profile
from apps.profiles.serializers import ProfileViewSerializer
from apps.auth.serializers import LoginSerializer
from apps.verification_codes.models import SmsCode
from apps.verification_codes.serializers import SMSVerificationSerializer
from apps.verification_codes.utils import send_sms

"""Render HTML"""


def updatecode_view(request):
    return render(request, 'updatecode.html')




"""Redirect after registration and authorization"""
def custom_login_redirect(request):
    redirect_url = request.session.get('redirect_url', '/default-url')
    return redirect(redirect_url)


"""Redirect for creating an API for authorization"""

def google_oauth_redirect(request):
    redirect_url = f"{settings.BASE_URL}/api/users/social-auth/login/google-oauth2/"
    return HttpResponseRedirect(redirect_url)

def facebook_oauth_redirect(request):
    redirect_url = f"{settings.BASE_URL}/api/users/social-auth/login/facebook/"
    return HttpResponseRedirect(redirect_url)

"""Authorization via Twilio"""

class SendSmsCode(CreateAPIView):
    def post(self, request, *args, **kwargs):
        code = SmsCode.objects.get(phone=request.data['phone'])
        if code and code.code_sent_time > timezone.now() - timedelta(seconds=60):
            return JsonResponse({"error_text": "too many attempts"}, 400)

        SmsCode.objects.create(phone=request.data['phone'], code=request.data['code'])

        return Response(
            {"detail": "Код отправлен."},
            status=status.HTTP_201_CREATED
        )


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone_number = serializer.validated_data['phone_number']

        try:
            profile = Profile.objects.get(phone=phone_number)
            profile.generate_sms_code()
            send_sms(phone_number, f"Your code is {profile.sms_code}")

            # Создайте токен и верните его
            token, created = Token.objects.get_or_create(user=profile.user)
            return Response({"token": token.key}, status=status.HTTP_200_OK)  # Возвратите токен

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
            code = SmsCode.objects.get(phone=phone_number)

            # Проверка срока действия кода
            if code.code_sent_time < timezone.now() - timedelta(seconds=60):
                return Response({"error": "Code expired"}, status=status.HTTP_400_BAD_REQUEST)

            profile.last_login_time = timezone.now()
            
            # Если у профиля нет пользователя, создаём его
            if profile.user is None:
                user = User.objects.create(username=profile.phone)
                profile.user = user
                profile.save()

            # Генерация токенов
            refresh = RefreshToken.for_user(profile.user)

            # Добавление URL для редиректа
            # if not profile.user.date_joined:
            request.session['redirect_url'] = f'https://freevet.me/verification/role?user_id={profile.user.id}'
            # else:
            #     request.session['redirect_url'] = f'https://freevet.me/main?user_id={profile.user.id}'
            
            redirect_url = request.session['redirect_url']

            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "redirect_url": redirect_url,
                "message": "Logged in"
            }, status=status.HTTP_200_OK)

        except Profile.DoesNotExist:
            return Response({"error": "Invalid code"}, status=status.HTTP_400_BAD_REQUEST)




class ProfileView(APIView):
    def get(self, request, pk):
        profile = Profile.objects.get(user_id=pk)
        serializer = ProfileViewSerializer(profile, context={'request': request})

        return Response(serializer.data, status=status.HTTP_200_OK)
