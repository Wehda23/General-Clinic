from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Staff, Doctor
from .serializer import StaffSerializer, DoctorSerializer, UserSerializer
from django.db.models import Q

# Create your views here.


class StaffView(APIView):
    def get(self, request, pk) -> Response:
        return Response("Staff")


class DoctorView(APIView):
    def get(self, request, pk) -> Response:
        # Grab the doctor
        doctor: Doctor = Doctor.objects.get(user__id=pk)
        print(doctor)
        return Response("Doctor")

    def delete(self, request, pk) -> Response:
        doctor: Doctor = Doctor.objects.get(user__id=pk).delete()
        return Response("Deleted Succesfully")


class ListStaffView(APIView):
    def get(self, request, pk) -> Response:
        return Response("Staff")


class ListDoctorView(APIView):
    def get(self, request, pk) -> Response:
        # Grab the doctor
        doctor: Doctor = Doctor.objects.get(user__id=pk)
        print(doctor)
        return Response("Doctor")
