from .models import *
from rest_framework import serializers


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model: Patient = Patient
        fields = "__all__"
