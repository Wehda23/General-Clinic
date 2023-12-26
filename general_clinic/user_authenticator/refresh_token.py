from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import BasePermission
from django.contrib.auth.models import User


# Create token Function
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }


class IsRefreshToken(BasePermission):
    def is_refresh_token_valid(self, refresh_token):
        try:
            decoded_token = RefreshToken(refresh_token)
            return decoded_token
        except Exception as e:
            return False

    def has_permission(self, request, view):
        """Method used to check refresh token"""
        data: dict = request.data

        if "refresh" not in data:
            return False

        refresh_token: str = request.data["refresh"]
        decoded_token = self.is_refresh_token_valid(refresh_token)
        if not decoded_token:
            return False

        # Grab the user
        user: User = User.objects.get(id=decoded_token["user_id"])
        request.user = user

        return True
