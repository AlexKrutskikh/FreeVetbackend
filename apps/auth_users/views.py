from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from django.conf import settings
from django.http import HttpResponseRedirect
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.utils import timezone
from datetime import timedelta
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from twilio.base.exceptions import TwilioRestException
from apps.profiles.models import Profile
from apps.profiles.serializers import ProfileViewSerializer
from apps.auth_users.serializers import LoginSerializer
from apps.verification_codes.serializers import SMSVerificationSerializer
from apps.verification_codes.utils import send_sms
from django.shortcuts import render

def updatecode_view(request):
    return render(request, 'updatecode.html')

"""API для авторизации и регистрации через социальные сети"""

def google_oauth_redirect(request):
    redirect_url = f"{settings.BASE_URL}/api/auth_users/social-auth/login/google-oauth2/"
    return HttpResponseRedirect(redirect_url)

def facebook_oauth_redirect(request):
    redirect_url = f"{settings.BASE_URL}/api/users/social-auth/login/facebook/"
    return HttpResponseRedirect(redirect_url)




"""Authorization via Twilio"""

class RegisterView(CreateAPIView):
    def post(self, request, *args, **kwargs):
        # Получаем данные из формы
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        photo = request.FILES.get('photo', None)

        # Проверка, переданы ли необходимые данные
        if not name or not phone:
            return Response(
                {"detail": "Необходимо указать имя и номер телефона."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Проверка, существует ли пользователь с данным номером телефона
        if Profile.objects.filter(phone=phone).exists():
            return Response(
                {"detail": "Пользователь уже зарегистрирован. Перейдите в окно входа."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Создаем новый профиль
        profile = Profile.objects.create(
            name=name,
            phone=phone,
            photo=photo  # Устанавливаем фото, если оно передано
        )
        
        # Генерируем и отправляем SMS-код
        profile.generate_sms_code()
        
        try:
            send_sms(profile.phone, f"Ваш код: {profile.sms_code}")
        except TwilioRestException:
            # Удаляем профиль, если SMS не может быть отправлено
            profile.delete()
            return Response(
                {"detail": "С текущими номерами отправителя и получателя SMS не может быть отправлено."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Возвращаем ответ об успешной регистрации
        return Response(
            {"detail": "Регистрация прошла успешно."},
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
            profile = Profile.objects.get(phone=phone_number, sms_code=code)

            # Проверка срока действия кода
            if profile.code_sent_time < timezone.now() - timedelta(seconds=90):
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
