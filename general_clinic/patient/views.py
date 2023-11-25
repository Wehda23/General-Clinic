from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Patient
from .serializer import PatientSerializer
from django.db.models import Q


# Create your views here.
class PatientDetails(APIView):
    def get(self, request, contact, format=None):
        # Check if the patient data exists
        if Patient.objects.filter(
            Q(email_address=contact) | Q(contact_info=contact)
        ).exists():
            # Grab the patient
            patient: Patient = Patient.objects.get(
                Q(email_address=contact) | Q(contact_info=contact)
            )
            # Serialize patient data
            patient_data: dict = PatientSerializer(patient).data

            return Response(patient_data, status=status.HTTP_200_OK)

        # In case failure or patient does not exists.
        return Response("Patient does not exists!", status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        pass

    def put(self, request):
        pass

    def delete(self, request):
        pass


# This view should be only for authenticated and staff members to see
class PatientsView(APIView):
    def get(self, request, format=None):
        return Response("Retrieving patients details")
