from django.urls import path
from .views import (
    EmployeeLoginView,
    staff_registeration,
    doctor_registeration,
)

urlpatterns = [
    path("login", EmployeeLoginView.as_view(), name="employee-login-view"),
    path("register/staff", staff_registeration, name="staff-register-view"),
    path("register/doctor", doctor_registeration, name="doctor-register-view"),
]
