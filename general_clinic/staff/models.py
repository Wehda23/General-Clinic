from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save, pre_delete
from django.dispatch import receiver
from django.db import IntegrityError
import uuid
import os


# Create your models here.
def profile_image_path(instance, filename):
    """
    This function is made to structure the path at which the image is going to be saved at.
    :instance: Class instance.
    :filename: The image file name.
    """
    return f"{instance.__class__.__name__}/{instance.__class__.__name__.lower()}_{instance.user.id}/{filename}"


class Employee(models.Model):
    # Id and Relationships
    user: User = models.OneToOneField(
        User, null=False, blank=False, on_delete=models.CASCADE
    )
    employee_id: models.UUIDField = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    # CharFields
    position: models.CharField = models.CharField(
        max_length=50, blank=False, null=False
    )
    contact_info: models.CharField = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )
    address: models.CharField = models.CharField(max_length=100, blank=True, null=True)
    # Media
    profile_image: models.ImageField = models.ImageField(
        upload_to=profile_image_path, default="default.png"
    )

    # Date and time fields
    date_of_birth: models.DateField = models.DateField(
        null=True, blank=True, editable=True
    )
    # Permissions
    allow_reschedule: models.BooleanField = models.BooleanField(
        null=True, blank=True, default=False
    )
    allow_delete_appointment: models.BooleanField = models.BooleanField(
        null=True, blank=True, default=False
    )

    class Meta:
        abstract = True
        ordering = ["user__id"]

    def __str__(self):
        employee = f"{self.user.username if self.user else None} {self.position} as {self.__class__.__name__}".title()
        return employee


class Staff(Employee):
    allow_appoint_doctor: models.BooleanField = models.BooleanField(
        null=True, blank=True, default=False
    )


class Doctor(Employee):
    is_verified: models.BooleanField = models.BooleanField(
        null=True, blank=True, default=False
    )
    is_available: models.BooleanField = models.BooleanField(
        null=True, blank=True, default=False
    )


# Delete image function
def delete_profile_image_and_folder(instance):
    """
    Function used to delete profile image upon deletion of the profile.
    """
    # Delete directory
    directory = os.path.dirname(instance.profile_image.path)
    if os.path.exists(directory):
        for root, dirs, files in os.walk(directory, topdown=False):
            for file in files:
                file_path = os.path.join(root, file)
                os.remove(file_path)
            for dir_name in dirs:
                dir_path = os.path.join(root, dir_name)
                os.rmdir(dir_path)
        os.rmdir(directory)


@receiver(pre_delete, sender=Doctor)
def deleteProfileImageAndFolder(sender, instance, using, **kwargs) -> None:
    """
    Function used to delete profile image upon deletion of the profile.
    """
    # Delete directory
    delete_profile_image_and_folder(instance)


@receiver(pre_delete, sender=Staff)
def deleteProfileImageAndFolder(sender, instance, using, **kwargs) -> None:
    """
    Function used to delete profile image upon deletion of the profile.
    """
    # Delete directory
    delete_profile_image_and_folder(instance)


def check_user_roles(instance, role_model, related_name, role_name):
    """
    Function to check if current instance does not have multiple roles

    Args:
        - instance: Model Instance
        - role_model: Model class Name
        - related_name: Model attribute related name in form of python str
        - role_name: instance role name in form of python str.
    """
    # Check if a related instance already exists in any other model
    related_instance = getattr(instance.user, related_name, None)
    if related_instance and related_instance != instance:
        # If a related instance exists, raise a validation error
        raise IntegrityError(f"User cannot have multiple {role_name} roles")


@receiver(pre_save, sender=Doctor)
def check_doctor_roles(sender, instance, **kwargs):
    check_user_roles(instance, Doctor, "staff", "Doctor")


@receiver(pre_save, sender=Staff)
def check_staff_roles(sender, instance, **kwargs):
    check_user_roles(instance, Staff, "doctor", "Staff")
