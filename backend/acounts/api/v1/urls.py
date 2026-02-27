from django.contrib import admin
from django.urls import path,include
from .views import (CustomObtainAuthToken,DestroyAuthToken,
                    CustomTokenObtainPairView,ChangePsswordView,
                    ProfileView,VerificationView,RegistrationView,ResendVerificationView,ResetPasswordView,PasswordConfirmView)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

urlpatterns = [
 
    path('registration/',view=RegistrationView.as_view(),name='registration'),
    #token authentication
    path("token/login/",view=CustomObtainAuthToken.as_view(),name='login'),
    path("token/logout/",view=DestroyAuthToken.as_view(),name='logout'),
    #jwt authentication
    path("jwt/create/",view=CustomTokenObtainPairView.as_view(),name='jwt-login'),
    path("jwt/refresh/",view=TokenRefreshView.as_view(),name='jwt-refresh'),
    path("jwt/verify/",view=TokenVerifyView.as_view(),name='jwt-verify'),
    #reset password
    path('change_password/',view=ChangePsswordView.as_view(),name='change_password'),
    #user profile
    path("profile/",view=ProfileView.as_view(),name='profile'),
    #verification
    path("verification/<str:token>/",VerificationView.as_view(),name='verification'),
    #resend Veification
    path("resend/verification/",view=ResendVerificationView.as_view(),name='resend_verification'),
    #reset password
    path("reset/password/",view=ResetPasswordView.as_view(),name='reset_password'),
    path("reset/password/confirm/<str:token>/",view=PasswordConfirmView.as_view(),name='password_confirm')
]