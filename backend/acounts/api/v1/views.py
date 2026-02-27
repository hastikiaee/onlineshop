from django.shortcuts import get_object_or_404
from rest_framework import generics,status
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated
from ...models import UserProfile,CustomUser
from .serializers import (ResgisterationSerializer,CustomTokenObtainPairSerializer,
                          CustomAuthTokenSerializer,ChangePasswordSerializer,UserProfileSerializer,
                          ResendVerificationSerializer,ResetPasswordSerializer,PasswordConfirmSerializer)
import threading
from django.core.mail import send_mail
from rest_framework_simplejwt.tokens import RefreshToken
import jwt
from myshop import settings
from jwt.exceptions import ExpiredSignatureError,InvalidTokenError
from django.utils import timezone
from datetime import datetime, timedelta

def create_toke_for_password(user_id):
    #ساخت توکن برای ریست کردن پسورد با تاربخ انقضای ۱۵ دقیقه ای
    now = timezone.now()
    payload = {
        "user_id": user_id,
        "type": "password_reset",   # مهم برای جدا کردن از access token
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(minutes=15)).timestamp())  # 15 دقیقه اعتبار
    }
    token=jwt.encode(payload,settings.SECRET_KEY,algorithm="HS256")
    return token



def get_tokens_for_user(user):
    # ساخت access token برای کاربر با استفاده از SimpleJWT
    refresh = RefreshToken.for_user(user)

    # فقط access token برگردانده می‌شود
    return str(refresh.access_token)


class EmailThread(threading.Thread):
    # یک ترد جدا برای ارسال ایمیل (تا درخواست اصلی بلاک نشود)
    def __init__(self, title,text,sender,to):
        super().__init__() 
        self.title=title
        self.text=text
        self.sender=sender
        self.to=to
    
    def  run(self):
        # متد run هنگام start شدن ترد اجرا می‌شود
        send_mail(
            self.title,
            self.text,
            self.sender,
            self.to,
            fail_silently=False
        )



class RegistrationView(generics.GenericAPIView):
    # ساخت کاربر جدید (در حالت unverified)
    # و ارسال ایمیل تایید که شامل jwt token است
    serializer_class=ResgisterationSerializer

    def post(self,request):
        
        # گرفتن دیتا و اعتبارسنجی
        serializer=self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        # ذخیره کاربر
        serializer.save()

        # گرفتن ایمیل کاربر ساخته شده
        email=serializer.instance.email
        data={"email":email}

        # گرفتن آبجکت کاربر از دیتابیس
        user=get_object_or_404(CustomUser,email=email)

        # ساخت access token برای کاربر
        token=get_tokens_for_user(user)

        # ارسال لینک تایید شامل توکن
        EmailThread(
            title='verification email',
            text=f'http://localhost:8000/acounts/api/v1/verification/{token}/',
            sender='from@gmail.com',
            to=[email]
        ).start()

        return Response(data)


class CustomObtainAuthToken(ObtainAuthToken):
    # لاگین با سیستم TokenAuthentication (توکن دیتابیسی)
    
    serializer_class=CustomAuthTokenSerializer

    def post(self, request, *args, **kwargs):
        # اعتبارسنجی اطلاعات لاگین
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # گرفتن یوزر از serializer
        user = serializer.validated_data['user']

        # ساخت یا گرفتن توکن
        token, created = Token.objects.get_or_create(user=user)

        # برگرداندن توکن + اطلاعات کاربر
        return Response({
            'token': token.key,
            'email':user.email,
            'user_id':user.id
        })
    
    
class DestroyAuthToken(APIView):
    # حذف توکن کاربر (logout)

    def post(self,request):
        request.user.auth_token.delete()
        return Response({'detail':"token has been sucessfully deleted  "})
    

class CustomTokenObtainPairView(TokenObtainPairView):
    # ویوی مربوط به دریافت access و refresh token از SimpleJWT
    serializer_class=CustomTokenObtainPairSerializer


class ChangePsswordView(generics.GenericAPIView):
    # تغییر رمز عبور (فقط برای کاربر لاگین شده)
    permission_classes=[IsAuthenticated]
    serializer_class=ChangePasswordSerializer

    def put(self,request):
        # ارسال instance=request.user برای تغییر پسورد همان کاربر
        serializer=self.serializer_class(
            data=request.data,
            instance=request.user,
            context={"request":request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'detail':"password changed successfully"})
    

class ProfileView(generics.RetrieveUpdateAPIView):
    # مشاهده و ویرایش پروفایل کاربر
    queryset=UserProfile
    serializer_class=UserProfileSerializer

    def get_object(self):
        # گرفتن پروفایل بر اساس کاربر لاگین شده
        user=self.request.user
        object=get_object_or_404(UserProfile,user=user)

        # ست کردن ایمیل از مدل User روی پروفایل
        object.email=user.email
        return object


class VerificationView(APIView):
    # تایید حساب کاربری از طریق JWT ارسال شده در لینک ایمیل
     
    def get(self,request,token):
        
        try:
            # دیکود کردن توکن با SECRET_KEY پروژه
            payload=jwt.decode(
                token,
                settings.SECRET_KEY,  
                algorithms=["HS256"]
            )
           
        # اگر توکن منقضی شده باشد
        except ExpiredSignatureError:
            return Response({"error": "Token expired"}, status=400)

        # اگر توکن نامعتبر باشد (امضا اشتباه یا دستکاری شده)
        except InvalidTokenError:
            return Response({"error": "Invalid token"}, status=400)

        # گرفتن user_id از payload
        user_id=payload["user_id"]

        # گرفتن کاربر از دیتابیس
        user=get_object_or_404(CustomUser,id=user_id)

        # تایید کاربر
        user.is_verified=True
        user.save()

        return Response({'detail':"your account was successfully verified"})
    
class ResendVerificationView(generics.GenericAPIView):
    serializer_class=ResendVerificationSerializer
    def post(self,request):
        #گرفتن ایمیل کاربر و فرستادن مجدد توکن به ایمیل
        serializer=self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user=serializer.validated_data['user']
        email=serializer.validated_data['email']
        token=get_tokens_for_user(user)

        # ارسال لینک تایید شامل توکن
        EmailThread(
            title='verification email',
            text=f'http://localhost:8000/acounts/api/v1/verification/{token}/',
            sender='from@gmail.com',
            to=[email]
        ).start()
        
        return Response({"detail":"ایمیل اعتبار سنجی مجددا ارسال شد"},status=status.HTTP_200_OK)
    
class ResetPasswordView(generics.GenericAPIView):
    #گرفتن ایمیل و فرستادن ایمیل بازیابی رمز عبور برای کاربر
    serializer_class=ResetPasswordSerializer
    def post(self,request):
        
        serializer=self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email=serializer.validated_data["email"]
        user=serializer.validated_data['user']
        token=create_toke_for_password(user.id)
        EmailThread(
            title='reset password',
            text=f'http://localhost:8000/acounts/api/v1/reset/password/confirm/{token}/',
            sender='from@gmail.com',
            to=[email]
        ).start()
        return Response({"detail":"ایمیل بازیابی رمز عبور ارسال شد"},status=status.HTTP_200_OK)

class PasswordConfirmView(generics.GenericAPIView):
    #encode کردن توکن و به دست اوردن id کاربر و عوض کردن پسورد 
    serializer_class=PasswordConfirmSerializer
    def patch(self,request,token):
        
        try:
            # دیکود کردن توکن با SECRET_KEY پروژه
            payload=jwt.decode(
                token,
                settings.SECRET_KEY,  
                algorithms=["HS256"]
            )
           
        # اگر توکن منقضی شده باشد
        except ExpiredSignatureError:
            return Response({"error": "Token expired"}, status=400)

        # اگر توکن نامعتبر باشد (امضا اشتباه یا دستکاری شده)
        except InvalidTokenError:
            return Response({"error": "Invalid token"}, status=400)
        
        if payload.get("type") != "password_reset":
            return Response({"error": "Invalid token type"}, status=400)

        user_id=payload["user_id"]
        user=get_object_or_404(CustomUser,id=user_id)
        serializer=self.serializer_class(data=request.data,instance=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail":"رمز عبور با موفقیت بازیابی شد"},status=status.HTTP_200_OK)
        