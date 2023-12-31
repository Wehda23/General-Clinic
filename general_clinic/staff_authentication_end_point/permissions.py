from rest_framework.permissions import BasePermission
from staff.models import Staff, Doctor
from django.contrib.auth.models import User, AnonymousUser

from .validators import EmailValidator


class IsStaff(BasePermission):
    """Class to check the permissions of the User"""

    def has_permission(self, request, view) -> bool:
        """Method request user"""
        # Write permissions are only allowed for staff users
        return request.user and request.user.is_staff


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
            if not "email" in request.user:
                return False
            # Check user is active or not
            return self.validate_user(request.data["email"])

        return request.user.is_active


class IsEmployee(BasePermission):
    """Class Check if user sender is an existing employee or not"""

    employee_models: tuple = (Staff, Doctor)

    def validate_data_keys(self, data: dict) -> bool:
        """
        Method used to check data keys

        Args:
            - data: A python dictionary that should only contain 2 keys (email, password)

        Returns:
            - True in case of success, False in case does not pass validation.
        """

        # Check number of keys
        if len(data.keys()) != 2:
            return False
        # Check keys
        if "email" not in data:
            return False
        if "password" not in data:
            return False
        return True

    def validate_employee(self, email: str) -> bool:
        """Check if the request.data is a valid employee email address"""
        # Validate Email format
        try:
            EmailValidator(email, ValueError).validate()
        except ValueError as e:
            return False

        # Check if employee exists in either employee model
        if not any(
            employee.objects.filter(user__email=email).exists()
            for employee in self.employee_models
        ):
            return False

        return True

    def has_permission(self, request, view) -> bool:
        """Method used to check if the request user is an existing employee"""
        data: dict = request.data

        # Check data.keys
        if not self.validate_data_keys(data):
            return False
        # Validate user email
        if not self.validate_employee(data["email"]):
            return False

        return True
