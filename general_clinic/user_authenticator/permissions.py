from rest_framework.permissions import BasePermission
from django.contrib.auth.models import User, AnonymousUser


class IsActive(BasePermission):
    """Class to Check if user is active or not"""

    def validate_user(self, email: str) -> bool:
        """Method to get the user by his email"""
        # Check if user exists
        if not User.objects.filter(email=email).exists():
            return False

        user: User = User.objects.get(email=email)

        return user.is_active

    def has_permission(self, request, view):
        """Method to check user"""
        if isinstance(request.user, AnonymousUser):
            # Check if key email exists, if not just return False.
            if not "email" in request.data:
                return False
            # Check user is active or not
            return self.validate_user(request.data["email"])

        return request.user.is_active
