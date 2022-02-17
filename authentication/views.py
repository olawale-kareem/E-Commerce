from django.http.request import RAISE_ERROR
from rest_framework import generics, status, views
from rest_framework.response import Response

# the token implementation
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from .utils import Util
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
import jwt                            # comes withthe simple jwt install
from django.conf import settings

# serializers
from .serializers import (RegisterSerializer, EmailVerificationSerializer, LoginSerializer,
                          ResetPasswordEmailRequestSerializer, SetNewPasswordSerializer,
                          CheckPasswordSerializer, LogoutSerializer)

# swagger
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# password reset
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .utils import Util
from rest_framework.exceptions import AuthenticationFailed

# logout views
from rest_framework import permissions

# renderers
from .renderers import UserRender


####

class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    renderer_classes = (UserRender,)

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        # validated credentials is use to create a user at this point
        serializer.save()
        user_data = serializer.data     # get the data out

        user = User.objects.get(email=user_data['email'])
        token = RefreshToken.for_user(user).access_token
        current_site = get_current_site(request).domain
        relative_link = reverse('email-verify')

        # email variables declaration and logic
        absurl = "http://"+current_site+relative_link+"?token=" + str(token)
        email_body = "Hi " + user.username + \
            " Use the link below to verify your email \n" + absurl
        data = {'email_body': email_body, 'to_email': user.email,
                'email_subject': 'Verify your email'}
        Util.send_email(data)

        return Response(user_data, status=status.HTTP_201_CREATED)


class VerifyEmail(views.APIView):
    serializer_class = EmailVerificationSerializer
    token_param_config = openapi.Parameter('token', in_=openapi.IN_QUERY,
                                           description='description', type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self, request):
        token = request.GET.get('token')

        try:
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms='HS256')
            user = User.objects.get(id=payload['user_id'])
            if not user.is_verified:
                user.is_verified = True
                user.save()
                data = {"email": "email is succefully registered"}
            return Response(data, status=status.HTTP_200_OK)

        except jwt.ExpiredSignatureError as identifier:
            data = {"error": "Activation link expired"}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

        except jwt.exceptions.DecodeError as identifier:
            data = {"error": "Invalid token"}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LogoutAPIView(generics.GenericAPIView):
    serializer_class = LogoutSerializer

    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_204_NO_CONTENT)


class RequestPasswordResetEmail(generics.GenericAPIView):
    serializer_class = ResetPasswordEmailRequestSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        email = request.data['email']
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            # mail body set up
            current_site = get_current_site(request=request).domain
            relative_link = reverse(
                'password-reset-confirm', kwargs={'uidb64': uidb64, 'token': token})
            absurl = "http://" + current_site + relative_link
            email_body = "Hello, \n Use the link to reset your password \n" + absurl
            data = {'email_body': email_body, 'to_email': user.email,
                    'email_subject': 'Reset your password'}
            Util.send_email(data)
            return Response({'success': 'we have sent you a link to reset the password'}, status=status.HTTP_200_OK)
        else:
            return Response({'Failed': 'Incorrect Email supplied'}, status=status.HTTP_400_BAD_REQUEST)


class PasswordTokenCheckAPI(generics.GenericAPIView):
    serializer_class = CheckPasswordSerializer

    def get(self, request, uidb64, token):
        try:
            id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({'error': 'Token not valid please request for a new one'})

            return Response({'success': True, 'message': 'Credentials Valid', 'uidb64': uidb64, 'token': token}, status=status.HTTP_200_OK)

        except DjangoUnicodeDecodeError as identifier:
            return Response({'error': 'invalid token'})


class SetNewPasswordAPIView(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request, uidb64):
        user_data = request.data
        try:
            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)
        except Exception as e:
            raise AuthenticationFailed('invalid uidb64 ', 400)
        else:
            password = user_data.get('new_password')
            confirm_password = user_data.get('confirm_password')
            print(password, confirm_password)
            if password != confirm_password:
                return Response({'failed': f'Password is not the same'}, status=status.HTTP_200_OK)
            user.set_password(password)
            user.save()
            return Response({'success': f'Password reset succesful'}, status=status.HTTP_200_OK)


class LogoutAPIView(generics.GenericAPIView):
    serializer_class = LogoutSerializer

    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_204_NO_CONTENT)


#######
# class RequestPasswordResetEmail(generics.GenericAPIView):

#     serializer_class = ResetPasswordEmailRequestSerializer

#     def post(self,request):
#         serializer = self.serializer_class(data=request.data)
#         email = request.data['email']
#         if User.objects.filter(email=email).exists():
#             user = User.objects.get(email=email)
#             uidb64 = urlsafe_base64_encode(smart_bytes(user.id))

#             current_site = get_current_site(request=request).domain
#             relative_link = reverse('password-reset-complete',kwargs={'uidb64':uidb64})
#             absurl = "http://" + current_site + relative_link
#             email_body = "Hello, \n Use the link to reset your password \n" + absurl
#             data = {'email_body': email_body, 'to_email': user.email,
#                     'email_subject': 'Reset your password'}
#             Util.send_email(data)
#             return Response({'success':'we have sent you a link to reset the password'}, status=status.HTTP_200_OK)
#         else:
#              return Response({'Failed':'Incorrect Email supplied'}, status=status.HTTP_400_BAD_REQUEST)
