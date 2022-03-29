from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.middleware import csrf
from rest_framework_simplejwt.views import TokenRefreshView

from .serializers import CookieTokenRefreshSerializer
from .utils import two_factor_authentication_send_email
from project import settings


class LoginAPIView(APIView):
    def post(self, request):
        data = request.data
        response = Response()
        username = data.get('username', None)
        password = data.get('password', None)
        otp_number = int(data.get('otpNumber', None))
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                if bool(otp_number):
                    if user.check_otp(otp_number):
                        user_tokens = user.get_tokens()
                        response.set_cookie(
                            key=settings.SIMPLE_JWT['AUTH_ACCESS_COOKIE'],
                            value=user_tokens["access"],
                            max_age=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'].total_seconds(),
                            secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
                            httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
                            samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
                        )
                        set_cookie_refresh_token(response, user_tokens["refresh"])
                        csrf.get_token(request)
                        response.data = {"Success": "Login successfully",
                                         "access_token_expire": settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
                                         "refresh_token_expire": settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME']}
                        return response
                    else:
                        return Response({"Error": "Invalid OTP number"})
                two_factor_authentication_send_email(user)
                return Response({"Message": "OTP number was send on your email"})
            else:
                return Response({"Error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({"Error": "Invalid username or password"}, status=status.HTTP_404_NOT_FOUND)


class CookieTokenRefreshView(TokenRefreshView):
    def finalize_response(self, request, response, *args, **kwargs):
        if response.data.get('refresh'):
            set_cookie_refresh_token(response, response.data["refresh"])
            del response.data['refresh']
        return super().finalize_response(request, response, *args, **kwargs)
    serializer_class = CookieTokenRefreshSerializer


def set_cookie_refresh_token(response, refresh_token):
    response.set_cookie(
        key=settings.SIMPLE_JWT['AUTH_REFRESH_COOKIE'],
        value=refresh_token,
        max_age=settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'].total_seconds(),
        secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
        httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
        samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE'],
    )

