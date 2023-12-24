from django.contrib import admin
from django.urls import path, include
from .views import StaffView, DoctorView

urlpatterns = [
    path("staff/<int:pk>", StaffView.as_view(), name="staff-view"),
    path("doctor/<int:pk>", DoctorView.as_view(), name="doctor-view"),
]
