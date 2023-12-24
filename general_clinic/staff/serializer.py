from .models import Doctor, Staff
from rest_framework import serializers
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model: User = User
        exclude: list = ["Username", "Password"]


class DoctorSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=True)

    class Meta:
        model: Doctor = Doctor
        fields = "__all__"


class StaffSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=True)

    class Meta:
        model: Staff = Staff
        fields = "__all__"
