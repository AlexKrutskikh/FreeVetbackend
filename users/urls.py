from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    custom_login_redirect,
    google_oauth_redirect,
    facebook_oauth_redirect
)
from .views import RegisterView, LoginView, VerifyCodeView
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [

    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('social-auth/',
         include('social_django.urls', namespace='social')), #social-auth

    path('redirect/', custom_login_redirect, name='custom_login_redirect'), #Redirect after registration and authorization

    path('login/google/', google_oauth_redirect, name='google-login-shortcut'), #Short API for authorization google

    path('login/facebook/', facebook_oauth_redirect, name='facebook-login-shortcut'), #Short API for authorization facebook

    path('register/', RegisterView.as_view(), name='register'),

    path('login/', LoginView.as_view(), name='login'),

    path('verify/', VerifyCodeView.as_view(), name='verify_code'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)