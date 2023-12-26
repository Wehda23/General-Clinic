from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from .serializer import UserLoginSerializer
from .refresh_token import IsRefreshToken, get_tokens_for_user

# Create your views here.
class LoginView(APIView):
    """
    This view will be used for the purpose of a user to Login/Register view.
    """

    # Login
    def get(self, request, *args, **kwargs) -> Response:
        """
        Get API view where the user uses to obtain a new Token.
        :args: Arguments.
        :kwargs: Keyword arguements.
        """
        patient_serializer: UserLoginSerializer = UserLoginSerializer(data=request.data)

        if patient_serializer.is_valid():
            return Response(patient_serializer.data, status=status.HTTP_200_OK)

        # Grab error
        error: str = patient_serializer.errors.get('non_field_errors', "Unknown error")[0]
        return Response(
            {"error": error},
            status=status.HTTP_404_NOT_FOUND)

    # Register User
    def post(self, request, *args, **kwargs):
        """
        Post API view where the patient registers a new account.
        :args: Arguments.
        :kwargs: Keyword arguements.
        """

        return Response("Register Patient")

    # forget password view
    def put(self, request, *args, **kwargs):
        """
        Put API view where the patient reset password view
        :args: Arguments.
        :kwargs: Keyword arguements.
        """

        return Response("Forgot password Patient")



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
