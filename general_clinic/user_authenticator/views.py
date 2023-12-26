from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from .serializer import UserLoginSerializer, UserRegisterSerializer
from .refresh_token import IsRefreshToken, get_tokens_for_user
from patient.models import Patient


def get_error(errors: list | dict) -> str:
    """Function used to grab or parse error message from errors

    Args:
        - errors: is a List | Dictionary like datastructure which contain error message.

    Returns:
        - error message as a string
    """
    if isinstance(errors, list):
        return errors[0]
    elif isinstance(errors, dict):
        try:
            key: str = list(errors.keys())[0]
            return errors[key][0]
        # Nested error
        except KeyError:
            nested_key: str = list(errors.keys())[0]
            return get_error(errors[nested_key])


# Create your views here.
class LoginView(APIView):
    """
    This view will be used for the purpose of a user to Login/Register view.
    """
    # Account Login
    def post(self, request, *args, **kwargs):
        """
        Get API view where the user uses to obtain a new Token.
        :args: Arguments.
        :kwargs: Keyword arguements.
        """
        patient_serializer: UserLoginSerializer = UserLoginSerializer(data=request.data)
        if patient_serializer.is_valid():
            return Response(patient_serializer.data, status=status.HTTP_201_CREATED)

        # Grab error
        error: str = get_error(patient_serializer.errors)
        return Response(error, status=status.HTTP_404_NOT_FOUND)

    # forget password view
    def put(self, request, *args, **kwargs):
        """
        Put API view where the patient reset password view
        :args: Arguments.
        :kwargs: Keyword arguements.
        """

        # Return Error Response incase error was raised
        return Response("Forgot password Patient")


@api_view(['POST'])
def patient_register(request, *args, **kwargs):
    """
    Post API view where the patient registers a new account.
    :args: Arguments.
    :kwargs: Keyword arguements.
    """
    # Get serializer
    new_patient: UserRegisterSerializer = UserRegisterSerializer(data=request.data)
    # Check if it passes validation or not
    if new_patient.is_valid():
        new_patient.save()
        return Response(
            "Account Registerated Successfully", status=status.HTTP_201_CREATED
        )

    # Grab error
    error: str = get_error(new_patient.errors)
    return Response(error, status=status.HTTP_406_NOT_ACCEPTABLE)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def patient_delete(request, *args, **kwargs):
        """
        Delete API view where the patient deletes their account
        :args: Arguments.
        :kwargs: Keyword arguements.
        """
        patient: Patient = request.user.patient
        patient.delete()
        # Return Error Response incase error was raised
        return Response("Patient Account Deletion is successful", status=status.HTTP_200_OK)

# Refresh Token View
@api_view(["POST"])
@permission_classes([IsRefreshToken])
def refresh_token(request):
    """
    Function used to refresh token of user
    :request: Request Object.
    """
    # get new tokens for patient
    tokens: dict = get_tokens_for_user(request.user)
    return Response(tokens, status=status.HTTP_202_ACCEPTED)
