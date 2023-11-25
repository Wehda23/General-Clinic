from django.contrib import admin
from django.urls import path, include
from .views import PatientDetails, PatientsView

urlpatterns = [
    path("", PatientsView.as_view(), name="patients-view"),
    path("<str:contact>", PatientDetails.as_view(), name="patient-details"),
]
