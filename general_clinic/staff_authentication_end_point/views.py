from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from staff_authentication_end_point.authenticators import IsStaff
from staff.models import Staff, Doctor
# Create your views here.



class StaffLoginView(APIView):
    """Staff Login View"""

    def post(self, request, *args, **kwargs):
        """Login post requests for staff"""
        data = request.data

        return Response("Staff Login View", status= status.HTTP_200_OK)
    
    def put(self,request, *args, **kwargs):
        """Forgot password view for staff"""

        return Response("Reset Password", status=status.HTTP_200_OK)
    
class DoctorLoginView(APIView):
    """Doctor Login View"""

    def post(self,request, *args, **kwargs):
        """Login post request for doctor"""
        data = request.data
        return Response("Doctor login view.", status=status.HTTP_200_OK)
    
    def put(self,request, *args,**kwargs):
        """Reset password for doctor"""
        data = request.data
        return Response("Doctor Forgot password view", status=status.HTTP_200_OK)


# We are going to create a staff registeration view which will require an authenticated member to register this new staff member
@api_view(['POST'])
@permission_classes([IsAuthenticated, IsStaff])
def staff_registeration(request, *args, **kwargs):
    """Register a new staff member."""

    return Response("Staff registeration under review", status=status.HTTP_200_OK)


# Any doctor can register their account normally with out having to be permitted
@api_view(['POST'])
def doctor_registeration(request, *args, **kwargs):
    """Register a new doctor to staff"""
    # Code to validate the doctor's credentials and save them in the database goes here
    
    return Response("Doctor registeration under review.")


