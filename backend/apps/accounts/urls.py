from django.urls import path

from .views import LoginAPIView, CookieTokenRefreshView, CurrentUserView, LogoutAPIView

urlpatterns = [
    path('login/', LoginAPIView.as_view()),
    path('logout/', LogoutAPIView.as_view()),
    path('refresh/', CookieTokenRefreshView.as_view()),
    path('user/', CurrentUserView.as_view()),
]
