from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Patient
from .serializer import PatientSerializer

# Create your views here.
class PatientDetails(APIView):
    def get(self, request, first_name, last_name, format=None):
        
        return Response(f"{first_name} {last_name}")


class PatientsView(APIView):
    def get(self, request, format=None):
        return Response("Retrieving patients details")
