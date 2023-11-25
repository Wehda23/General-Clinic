from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save, pre_delete
from django.dispatch import receiver
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
    first_name: models.CharField = models.CharField(
        max_length=50, blank=False, null=False
    )
    last_name: models.CharField = models.CharField(
        max_length=50, blank=False, null=False
    )
    position: models.CharField = models.CharField(
        max_length=50, blank=False, null=False
    )
    contact_info: models.CharField = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )
    # Media
    profile_image: models.ImageField = models.ImageField(
        upload_to=profile_image_path, default="default.png"
    )

    # Date and time fields
    date_of_birth: models.DateField = models.DateField(
        null=True, blank=True, editable=True
    )

    class Meta:
        abstract = True


class Staff(Employee):
    pass


class Doctor(Employee):
    pass


@receiver(pre_delete, sender=Doctor)
def deleteProfileImageAndFolder(sender, instance, using, **kwargs) -> None:
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

@receiver(pre_delete, sender=Staff)
def deleteProfileImageAndFolder(sender, instance, using, **kwargs) -> None:
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
