from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from .permissions import (
    IsStaff,
    IsEmployee,
    IsActive,
)
from .serializers import (
    EmployeeLoginSerializer,
    StaffUserRegisterationSerializers,
    DoctorUserRegisterationSerializer,
)
from staff.models import Staff, Doctor


# Function that parses an error
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
class EmployeeLoginView(APIView):
    """Employee Login View"""

    permission_classes = (IsEmployee, IsActive)

    def post(self, request, *args, **kwargs):
        """Login post requests for Employee"""
        data: dict = request.data

        employee_serializer: EmployeeLoginSerializer = EmployeeLoginSerializer(
            data=data
        )
        # validate Employee
        if employee_serializer.is_valid():
            # Grab validated data
            employee_data: dict = employee_serializer.validated_data
            return Response(employee_data, status=status.HTTP_202_ACCEPTED)
        # Grab error
        error: str = get_error(employee_serializer.errors)
        return Response(error, status=status.HTTP_406_NOT_ACCEPTABLE)

    def put(self, request, *args, **kwargs):
        """Forgot password view for Employee"""

        return Response("Reset Password", status=status.HTTP_200_OK)


# We are going to create a staff registeration view which will require an authenticated member to register this new staff member
@api_view(["POST"])
@permission_classes([IsAuthenticated, IsStaff, IsActive])
def staff_registeration(request, *args, **kwargs):
    """Register a new staff member."""
    staff_serializer = StaffUserRegisterationSerializers(data=request.data)

    if staff_serializer.is_valid():
        # Register new staff member
        staff_user = staff_serializer.save()
        # Assign permissions to the user
        staff_user.is_active = False
        staff_user.save()
        # Create a function that sends a message to email.
        # Once verified convert User.is_active to True
        return Response(
            "Please open your mail to activate your staff account.",
            status=status.HTTP_201_CREATED,
        )
    # Grab error
    error: str = get_error(staff_serializer.errors)
    return Response(error, status=status.HTTP_200_OK)


# Any doctor can register their account normally with out having to be permitted
@api_view(["POST"])
def doctor_registeration(request, *args, **kwargs):
    """Register a new doctor to staff"""
    # Code to validate the doctor's credentials and save them in the database goes here
    # create DoctorSerializer
    doctor_serializer = DoctorUserRegisterationSerializer(data=request.data)
    # Validate the serializer
    if doctor_serializer.is_valid():
        # Create new User, Doctor
        doctor_user = doctor_serializer.save()
        # Assign permissions to the doctor_user
        doctor_user.is_active = False
        doctor_user.save()
        # Create a function that sends a message to email.
        # Once verified convert User.is_active to True
        return Response(
            "Please visit to your email to activate your account.",
            status=status.HTTP_201_CREATED,
        )
    # Grab error
    error: str = get_error(doctor_serializer.errors)
    return Response(error, status=status.HTTP_403_FORBIDDEN)
