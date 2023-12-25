from django.contrib import admin
from django.urls import path, include
from .views import LoginView, refresh_token

urlpatterns = [
    path("", LoginView.as_view(), name="client-login-view"),
    path("refresh", refresh_token, name="client-refresh-token-view"),
]
