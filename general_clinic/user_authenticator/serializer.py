from rest_framework import serializers
from patient.models import Patient
from django.contrib.auth.models import User
from .refresh_token import get_tokens_for_user
from .validators import (
    EmailValidator,
    NameValidator,
    DateValidator,
    PasswordValidator,
)

# Create A Patient's Serializer
class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model: Patient = Patient
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    patient: PatientSerializer = PatientSerializer(read_only=True)

    class Meta:
        model: User = User
        fields = [
            "email",
            "first_name",
            "last_name",
            "username",
            "patient",
        ]

    def to_representation(self, instance):
        """Perform few tasks everything time this serializer is called"""
        user: User = User.objects.get(email=instance.email)
        # Update patient age everytime instance is called.
        user.patient.set_age

        return super().to_representation(instance)


# Create A UserSerializer
class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model: User = User
        fields: tuple = (
            "email",
            "password",
        )
        extra_kwargs: dict = {
            "password": {"write_only": True, "required": True},
            "email": {"required": True},
        }

    def validate(self, attr):
        """Validation methode for User instance."""
        # Check Email
        if not User.objects.filter(email=attr["email"]).exists():
            raise serializers.ValidationError("Patient Does not exist.")
        user: User = User.objects.get(email=attr["email"])
        # Check Password
        if not user.check_password(attr["password"]):
            raise serializers.ValidationError("Patient Email or Password is Incorrect.")
        return attr

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # Get the email
        email: str = data.pop("email")
        # Get user object
        user: User = User.objects.get(email=email)
        # Get Serialized data
        data: dict = UserSerializer(user).data
        # add Token Field
        data["token"] = get_tokens_for_user(user)
        return data


# Create a serializer for patient Registeration.
class PatientRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model: Patient = Patient
        fields: tuple = ("address", "contact_info", "date_of_birth")
        extra_kwargs: dict = {
            "address": {"required": True},
            "contact_info": {"required": True},
            "date_of_birth": {"required": True},
        }

# Create Serializer for user registeration.
class UserRegisterSerializer(serializers.ModelSerializer):
    patient = PatientRegisterSerializer()

    class Meta:
        model: User = User
        fields = ("first_name", "last_name", "email", "password", "patient")
        extra_kwargs: dict = {
            "password": {"write_only": True, "required": True},
            "email": {"required": True},
            "first_name": {"required": True},
            "last_name": {"required": True},
            "patient": {"required": True},
        }

    def validate_first_name(self, value):
        """Method to Validate first name"""
        # validate first name
        NameValidator(value, serializers.ValidationError).validate()
        return value
    
    def validate_last_name(self, value):
        """Method to Validate last name"""
        # validate last name
        NameValidator(value, serializers.ValidationError).validate()
        return value
    
    def validate_email(self, value):
        """
        Method validates email format
        """
        # Validate Email
        EmailValidator(value, serializers.ValidationError).validate()
        return value

    def validate_password(self, value):
        """Method Validates Password"""
        # Validate password
        PasswordValidator(value, serializers.ValidationError).validate()
        return value

    def validate(self, attrs):
        """Method used to validate registeration of a new patient account"""
        # Need to check if there is not another user already with same email
        if User.objects.filter(email= attrs['email']).exists():
            # Raise account already exists
            raise serializers.ValidationError("Patient account with this email already exists")
        
        return attrs

    def create(self, validated_data, *args, **kwargs):
        """Method used to create a new User and Patient Instance"""
        patient_data = validated_data.pop('patient')
        
        # Create the user instance
        validated_data['username'] = " "
        user = User.objects.create_user(**validated_data)
        user.username = user.first_name + " " + user.last_name
        user.save()
        #Create the patient instance
        new_patient: Patient = Patient.objects.create(**patient_data, user = user)
        new_patient.set_age
        new_patient.save()
        
        return user
