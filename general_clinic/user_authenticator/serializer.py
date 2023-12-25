from rest_framework import serializers
from patient.models import Patient
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken


# Create token Function
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

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
        if not User.objects.filter(email=attr['email']).exists():
            raise serializers.ValidationError("Patient Does not exist.")
        user: User = User.objects.get(email= attr['email'])
        # Check Password
        if not user.check_password(attr["password"]):
            raise serializers.ValidationError("Patient Email or Password is Incorrect.")
        return attr
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        # Get the email
        email: str = data.pop('email')
        # Get user object
        user: User = User.objects.get(email=email)
        # Get Serialized data
        data: dict = UserSerializer(user).data
        # add Token Field
        data['token'] = get_tokens_for_user(user)
        return data

