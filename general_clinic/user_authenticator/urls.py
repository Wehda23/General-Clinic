from django.urls import path
from .views import LoginView, refresh_token, patient_delete, patient_register

urlpatterns = [
    path("", LoginView.as_view(), name="client-login-view"),
    path("refresh", refresh_token, name="client-refresh-token-view"),
    path("create", patient_register, name="client-account-create"),
    path("delete", patient_delete, name="client-account-delete"),
]
