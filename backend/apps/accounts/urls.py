from django.urls import path

from .views import LoginAPIView, CookieTokenRefreshView

urlpatterns = [
    path('login/', LoginAPIView.as_view()),
    path('refresh/', CookieTokenRefreshView.as_view()),
]
