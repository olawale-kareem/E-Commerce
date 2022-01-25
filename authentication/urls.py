from django.urls import path
from .views import (RegisterView, VerifyEmail, LoginAPIView,
                    LogoutAPIView, RequestPasswordResetEmail, SetNewPasswordAPIView)

from rest_framework_simplejwt.views import (
    TokenRefreshView,
)


urlpatterns = [

    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('logout/', LogoutAPIView.as_view(), name="logout"),
    path('email-verify/', VerifyEmail.as_view(), name='email-verify'),

    path('request-reset-email/', RequestPasswordResetEmail.as_view(),
         name='forget-password'),
    path('password-reset/<uidb64>/', SetNewPasswordAPIView.as_view(),
         name='password-reset-complete'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh')
]
