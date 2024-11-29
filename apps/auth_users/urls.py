from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    google_oauth_redirect,
    facebook_oauth_redirect, ProfileView
)
from .views import RegisterView, LoginView, VerifyCodeView, updatecode_view
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [

    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),


    path('social-auth/',
         include('social_django.urls', namespace='social')),                          # api библиотеки social-auth-app-django

    path('login/google/', google_oauth_redirect, name='google-login-shortcut'),       # регистрация и авторизация google

    path('login/facebook/', facebook_oauth_redirect, name='facebook-login-shortcut'), # регистрация и авторизация google facebook


    path('register/', RegisterView.as_view(), name='register'),


    path('login/', LoginView.as_view(), name='login'),

    path('verify/', VerifyCodeView.as_view(), name='verify_code'),

    path('profile/<pk>', ProfileView.as_view(), name='profile'),

    path('1', updatecode_view, name='1'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
