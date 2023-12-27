from rest_framework.permissions import BasePermission




class IsStaff(BasePermission):
    """ Class to check the permissions of the User """
    def has_permission(self, request, view):
        """Method request user"""
        # Write permissions are only allowed for staff users
        return super().has_permission(request, view)