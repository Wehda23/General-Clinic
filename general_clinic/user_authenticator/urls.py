from django.contrib import admin
from django.urls import path, include
from .views import LoginView

urlpatterns = [
   path("", LoginView.as_view(), name="client-login-view"),

]
