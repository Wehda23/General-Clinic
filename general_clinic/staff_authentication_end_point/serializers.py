from rest_framework import serializers
from django.contrib.auth.models import User
from staff.models import Doctor, Staff
from .refresh_token import get_tokens_for_user
from .validators import (
    EmailValidator,
    NameValidator,
    PasswordValidator,
)


# Create Staff Serializer
class StaffSerializer(serializers.ModelSerializer):
    class Meta:
        model: Staff = Staff
        exclude = ["user"]


# Create Doctor Serializer
class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model: Doctor = Doctor
        exclude = ["user"]


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


# ------------------------------- STAFF RELATED Registeration SERIALIZERS ---------------------------- #


class StaffRegisterationSerializer(serializers.ModelSerializer):
    class Meta:
        model: Staff = Staff
        fields: tuple = (
            "address",
            "position",
            "contact_info",
            "date_of_birth",
        )
        extra_kwargs: dict = {
            "address": {"required": True},
            "position": {"required": True},
            "contact_info": {"required": True},
            "date_of_birth": {"required": True},
        }


# Employee Registeration Serializers
class StaffUserRegisterationSerializers(serializers.ModelSerializer):
    staff = StaffRegisterationSerializer()

    class Meta:
        model: User = User
        fields = ("first_name", "last_name", "email", "password", "staff")
        extra_kwargs: dict = {
            "password": {"write_only": True, "required": True},
            "email": {"required": True},
            "first_name": {"required": True},
            "last_name": {"required": True},
            "staff": {"required": True},
        }
    def validate_first_name(self, name) -> str:
        """Method to validate first name"""
        # validate
        NameValidator(name, serializers.ValidationError).validate()
        return name

    def validate_last_name(self, name) -> str:
        """Method to validate first name"""
        # validate
        NameValidator(name, serializers.ValidationError).validate()
        return name

    def validate_password(self, password) -> str:
        """Method to validate password"""
        # Validate
        PasswordValidator(password, serializers.ValidationError).validate()
        return password

    def validate_email(self, email) -> str:
        """Validate email"""
        # validate
        EmailValidator(email, serializers.ValidationError).validate()
        return email
    
    def validate(self, attrs) -> dict:
        """method to validate data"""

        # Check if a user with this email already exists or not
        if User.objects.filter(email=attrs["email"]).exists():
            # Raise error
            raise serializers.ValidationError("Email is already registered")

        return attrs

    def create(self, validated_data, *args, **kwargs):
        """Method used to create a new instance of the serializer class Model"""
        # get new staff data
        staff_data = validated_data.pop("staff")
        # Create User name functionality here, you can make it so that it recreates a unique username to avoid errors.
        username: str = (
            validated_data["first_name"]
            + "-"
            + validated_data["last_name"]
            + "#"
            + validated_data["date_of_birth"]
        )
        # Create user
        user: User = User.objects.create_user(**validated_data, username=username)
        # Create new staff and set User to staff.
        new_staff: Staff = Staff.objects.create(**staff_data, user=user)
        # set staff to inactive
        # Return created user
        return user


class DoctorRegisterationSerializer(serializers.ModelSerializer):
    class Meta:
        model: Doctor = Doctor
        fields: tuple = (
            "address",
            "position",
            "contact_info",
            "date_of_birth",
        )
        extra_kwargs: dict = {
            "address": {"required": True},
            "position": {"required": True},
            "contact_info": {"required": True},
            "date_of_birth": {"required": True},
        }


class DoctorUserRegisterationSerializer(serializers.ModelSerializer):
    doctor = DoctorRegisterationSerializer()

    class Meta:
        model: User = User
        fields: tuple = ("first_name", "last_name", "email", "password", "doctor")
        extra_kwargs: dict = {
            "password": {"write_only": True, "required": True},
            "email": {"required": True},
            "first_name": {"required": True},
            "last_name": {"required": True},
            "doctor": {"required": True},
        }

    def validate_first_name(self, name) -> str:
        """Method to validate first name"""
        # validate
        NameValidator(name, serializers.ValidationError).validate()
        return name

    def validate_last_name(self, name) -> str:
        """Method to validate first name"""
        # validate
        NameValidator(name, serializers.ValidationError).validate()
        return name

    def validate_password(self, password) -> str:
        """Method to validate password"""
        # Validate
        PasswordValidator(password, serializers.ValidationError).validate()
        return password

    def validate_email(self, email) -> str:
        """Validate email"""
        # validate
        EmailValidator(email, serializers.ValidationError).validate()
        return email

    def validate(self, attrs) -> dict:
        """method to validate data"""

        # Check if a user with this email already exists or not
        if User.objects.filter(email=attrs["email"]).exists():
            # Raise error
            raise serializers.ValidationError("Email is already registered")

        return attrs

    def create(self, validated_data, *args, **kwargs):
        """Create new user instance with validated data and add it to the database."""
        # get new doctor data
        doctor_data = validated_data.pop("doctor")
        # Create User name functionality here, you can make it so that it recreates a unique username to avoid errors.
        username: str = (
            validated_data["first_name"]
            + "-"
            + validated_data["last_name"]
            + "#"
            + validated_data["date_of_birth"]
        )
        # Create user
        user: User = User.objects.create_user(**validated_data, username=username)
        # Create new doctor and set User to Doctor.
        new_doctor: Doctor = Doctor.objects.create(**doctor_data, user=user)
        # set doctor to inactive
        # Return created user
        return user
