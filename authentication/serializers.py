from django.db.models import fields
from rest_framework import serializers
from .models import User

# login
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed

# set new password serializer
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

# logout
from rest_framework_simplejwt.tokens import RefreshToken, TokenError



class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)

    class Meta:
        model = User
        fields = ['email','username','password']

    def validate(self, attrs):
        email = attrs.get('email', '')
        username = attrs.get('username', '')

        if not username.isalnum():
            raise serializers.ValidationError('The username should only contain alphanumeric')
        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length = 555)
    class Meta:
        model = User
        fields = ['token']

class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=3 )
    password = serializers.CharField(max_length=68, min_length=6, write_only = True )
    username = serializers.CharField(max_length=255, min_length=3, read_only = True )
    tokens = serializers.CharField(max_length=68, min_length=6, read_only = True  )    

    class Meta:
        model = User
        fields = [ 'email', 'password', 'username', 'tokens']

    def validate(self, attrs):
        email = attrs.get('email', ' ')
        password = attrs.get('password', ' ')
        user = auth.authenticate(email=email, password=password)

        if not user:
            raise AuthenticationFailed('Invalid credentials, try again')
        if not user.is_active:
            raise AuthenticationFailed('Account is disabled, contact admin')
        if not user.is_verified:
            raise AuthenticationFailed('Email is not verified')

        return{
            'email': user.email,
            'username': user.username,
            'tokens': user.tokens
        }

class ResetPasswordEmailRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length = 2)
    class Meta:
        fields = ['email']

class CheckPasswordSerializer(serializers.Serializer):
    token = serializers.CharField(min_length=1,  write_only=True)
    uidb64 = serializers.CharField(min_length=1,  write_only=True)

    class Meta:
        fields = ['token', 'uidb64']

class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(min_length=6, max_length=68, write_only=True)
    token = serializers.CharField(min_length=1,  write_only=True)
    uidb64 = serializers.CharField(min_length=1,  write_only=True)

    class Meta:
        fields = ['password', 'token', 'uidb64']

    def validate(self, attrs):
        try:
            password = attrs.get('password')
            token = attrs.get('token')
            uidb64 = attrs.get('uidb64')
            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)
            if not PasswordResetTokenGenerator.check_token(user=user, token=token):
                raise AuthenticationFailed('The reset link is invalid', 401)
            user.set_password(password)
            user.save()
            return(user)
        except Exception as e :
            print(e)
            raise AuthenticationFailed('The reset link is invalid', 401)
     
class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    default_error_message = {
        'bad_token': ('Token is expired or invalid')
    }

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):

        try:
            RefreshToken(self.token).blacklist()

        except TokenError:
            self.fail('bad_token')


###

# class ResetPasswordEmailRequestSerializer(serializers.Serializer):
#     email = serializers.EmailField(min_length = 2)
#     class Meta:
#         fields = ['email']

# class SetNewPasswordSerializer(serializers.Serializer):
#     new_password = serializers.CharField(min_length=6, max_length=68, write_only=True)
#     confirm_password = serializers.CharField(min_length=6, max_length=68, write_only=True)
#     uidb64 = serializers.CharField(min_length=1,  read_only=True)

#     class Meta:
#         fields = ['password', 'confirm_password', 'uidb64']