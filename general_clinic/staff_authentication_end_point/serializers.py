from rest_framework import serializers
from django.contrib.auth.models import User
from staff.models import Doctor, Staff
from .refresh_token import get_tokens_for_user


# Create Staff Serializer
class StaffSerializer(serializers.ModelSerializer):
    class Meta:
        model: Staff = Staff
        exclude = ['user']


# Create Doctor Serializer
class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model: Doctor = Doctor
        exclude = ['user']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model: User = User
        fields = [
            "email",
            "first_name",
            "last_name",
            "username",
        ]


class EmployeeLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model: User = User
        fields = ["email", "password"]
        extra_kwargs: dict = {
            "email": {"required": True},
            "password": {"required": True},
        }

    def get_employee(self, employee: User) -> dict:
        """Method to get employee"""
        if hasattr(employee, "staff"):
            return StaffSerializer(employee.staff).data
        elif hasattr(employee, "doctor"):
            return DoctorSerializer(employee.doctor).data
        else:
            raise serializers.ValidationError("Employee is not a valid user")
                

    def validate(self, attrs) -> dict:
        """Method used to validate User"""

        # Check if user exists
        if not User.objects.filter(email=attrs["email"]).exists():
            raise serializers.ValidationError("Employee Does not exists.")

        # Get Employee
        employee = User.objects.get(email=attrs["email"])

        # Check password
        if not employee.check_password(attrs["password"]):
            raise serializers.ValidationError("Employee Email or Password is incorrect")

        # Grab employee Data
        employee_data: dict = self.get_employee(employee)

        # Create token (Access, Refresh)
        token: dict = get_tokens_for_user(employee)
        # Add Token data to employee data and return it
        return {**UserSerializer(employee).data, **employee_data, "token": token}


# Employee Registeration Serializers 
class StaffRegisterationSerializers(serializers.ModelSerializer):
    class Meta:
        model: User = User
        fields = "__all__"

    def validate(self, attrs) -> dict:
        """method to validate data"""

class DoctorRegisterationSerializer(serializers.ModelSerializer):
    class Meta:
        model: User = User
        fields = "__all__"
    
    def validate(self, attrs) -> dict:
        """method to validate data"""
        
    
