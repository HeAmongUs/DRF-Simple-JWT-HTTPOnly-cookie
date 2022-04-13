from datetime import timedelta

from django.contrib.auth import authenticate
from rest_framework import status, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.middleware import csrf
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView

from .serializers import CookieTokenRefreshSerializer, AccountSerializer
from .utils import two_factor_authentication_send_email
from project import settings


class LoginAPIView(APIView):
    def post(self, request):
        data = request.data
        response = Response()
        username = data.get('username', None)
        password = data.get('password', None)
        otp_number = int(data.get('otpNumber', 0)) or 0
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                if bool(otp_number):
                    if user.check_otp(otp_number):
                        user_tokens = user.get_tokens()
                        set_cookie_token(response, user_tokens["access"], "ACCESS")
                        set_cookie_token(response, user_tokens["refresh"], "REFRESH")
                        csrf.get_token(request)
                        response.data = {
                            "Success": "Login successfully",
                        }
                        return response
                    else:
                        return Response({"Error": "Invalid OTP number"})
                two_factor_authentication_send_email(user)
                return Response({"Message": "OTP number was send on your email"})
            else:
                return Response({"Error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({"Error": "Invalid username or password"}, status=status.HTTP_404_NOT_FOUND)


class LogoutAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def delete(self, request):
        response = Response()
        try:
            set_cookie_token(response, "logoutToken", "REFRESH", timedelta(seconds=-1).total_seconds())
            set_cookie_token(response, "logoutToken", "ACCESS", timedelta(seconds=-1).total_seconds())
            refresh_token = RefreshToken(request.COOKIES.get('refresh_token'))
            refresh_token.blacklist()
            response.status_code = 205
            return response
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class CurrentUserView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        serializer = AccountSerializer(request.user)
        return Response(serializer.data)


class CookieTokenRefreshView(TokenRefreshView):
    def finalize_response(self, request, response, *args, **kwargs):
        if response.data.get('refresh'):
            set_cookie_token(response, response.data["refresh"], "REFRESH")
            del response.data['refresh']
        if response.data.get('access'):
            set_cookie_token(response, response.data["access"], "ACCESS")
            del response.data['access']
        return super().finalize_response(request, response, *args, **kwargs)

    serializer_class = CookieTokenRefreshSerializer


def set_cookie_token(response, token_value, token_type, cookie_max_age=None):
    if token_type not in ["ACCESS", "REFRESH"]:
        raise ValueError("Invalid token_type")
    response.set_cookie(
        key=settings.SIMPLE_JWT[f'AUTH_{token_type}_COOKIE'],
        value=token_value,
        max_age=int(cookie_max_age or settings.SIMPLE_JWT[f'{token_type}_TOKEN_LIFETIME'].total_seconds()),
        secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
        httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
        samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE'],
    )
