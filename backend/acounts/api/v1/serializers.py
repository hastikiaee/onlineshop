from rest_framework import serializers

from ...models import CustomUser,UserProfile
from django.core import exceptions
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer



class ResgisterationSerializer(serializers.ModelSerializer):

    password2=serializers.CharField(max_length=16,write_only=True)
    
    class Meta:
        model=CustomUser
        fields=['email','password','password2']
 
    def validate(self, attrs):
        password2=attrs['password2']
        password=attrs['password']
        if password!=password2:
            raise serializers.ValidationError({"detail":"password and password2 do not match"})
        email=attrs['email']
        user=CustomUser(email=email)

        erros=dict()
        
        try:
            validate_password(password=password,user=user)
        except exceptions.ValidationError as e:
            erros['password']=list(e.message)

        if erros:
            raise serializers.ValidationError(erros)

        return attrs
    
    def create(self, validated_data):
        validated_data.pop("password2")
        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user
    
class CustomAuthTokenSerializer(serializers.Serializer):
    email = serializers.CharField(
        label=_("Email"),
        write_only=True
    )
    password = serializers.CharField(
        label=_("Password"),
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )
    token = serializers.CharField(
        label=_("Token"),
        read_only=True
    )

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'),
                                email=email, password=password)

            # The authenticate call simply returns None for is_active=False
            # users. (Assuming the default ModelBackend authentication
            # backend.)
            if not user:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Must include "username" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
   

    def validate(self,attrs) :
        data = super().validate(attrs)
        email=self.user.email
        user_id=self.user.id
        data['email']=email
        data['user_id']=user_id
        return data
    
class ChangePasswordSerializer(serializers.Serializer):
    #change password serializer 
    old_password=serializers.CharField(required=True)
    password=serializers.CharField(required=True)
    password2=serializers.CharField(required=True)

    def validate(self, attrs):
        
        request=self.context.get('request')
        user=request.user
        if not user.check_password(attrs['old_password']):
            raise serializers.ValidationError({'detail': "رمز عبور اشتباه است"})
        if attrs['password']!=attrs['password2']:
            raise serializers.ValidationError({"detail":"password and password2 do not match"})

        errors=dict()
        try:
            validate_password(password=attrs['password'],user=user)
        except exceptions.ValidationError as e:
            errors['password']=list(e.messages)
        if errors:
            raise serializers.ValidationError(errors)
        return attrs
    
    def update(self, instance, validated_data):
        instance.set_password(validated_data['password'])
        instance.save()
        return instance

class UserProfileSerializer(serializers.ModelSerializer):
    
    email=serializers.EmailField(read_only=True)
    class Meta:
        model=UserProfile
        fields=['id','email','last_name','first_name']

class ResendVerificationSerializer(serializers.Serializer):
    email=serializers.EmailField(required=True)

    def validate(self, attrs):
        email=attrs['email']
        user=get_object_or_404(CustomUser,email=email)
        if user.is_verified:
            raise serializers.ValidationError({"detail":"هویت کاربر قبلا تایید شده"})
        attrs['user']=user
        return attrs

class ResetPasswordSerializer(serializers.Serializer):

    email=serializers.EmailField(required=True)

    def validate(self,attrs):
    
        email=attrs['email']
        user=get_object_or_404(CustomUser,email=email)
        attrs['user']=user
        return attrs
        
       
class PasswordConfirmSerializer(serializers.Serializer):

    password=serializers.CharField(required=True,write_only=True)
    password2=serializers.CharField(required=True,write_only=True)
    
    def validate(self, attrs):
        
        if attrs['password']!=attrs['password2']:
            raise serializers.ValidationError({"detail":"password and password2 do not match"})

        errors=dict()
        try:
            validate_password(password=attrs['password'])
        except exceptions.ValidationError as e:
            errors['password']=list(e.messages)
        if errors:
            raise serializers.ValidationError(errors)
        return attrs
    
    def update(self, instance, validated_data):
        validated_data.pop("password2")
        instance.set_password(validated_data['password'])
        instance.save()
        return instance
    