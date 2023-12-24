from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.views import APIView
from ..patient.models import Patient
from ..patient.serializer import PatientSerializer
# Create your views here.


class LoginView(APIView):

    def get(self, pk) -> Response:
        
        return Response("Login")