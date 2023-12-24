from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from patient.serializer import PatientSerializer


# Create your views here.
class LoginView(APIView):
    """
    This view will be used for the purpose of a user to Login/Register view.
    """
    # Login
    def get(self, *args, **kwargs) -> Response:
        """
        Get API view where the user uses to obtain a new Token.
        :args: Arguments.
        :kwargs: Keyword arguements.
        """
        return Response("Login")
    
    # Register User
    def post(self, request, *args, **kwargs):
        """
        Post API view where the patient registers a new account.
        :args: Arguments.
        :kwargs: Keyword arguements.
        """

        return Response("Register Patient")


# Refresh Token View
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def refresh_token(request):
    """
    Function used to refresh token of user
    :request: Request Object.
    """
    return Response("Refresh Token View.")

