from django.db import models
from django.contrib.auth.models import User
from datetime import date
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

"""sql
CREATE TABLE Patient (
    Patient_ID UUID PRIMARY KEY,
    Date_of_Birth DATE,
    Contact_Info VARCHAR(100),
    Address VARCHAR(100)
);
"""


class Patient(models.Model):
    # Char Fields
    id: models.UUIDField = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    user: User = models.OneToOneField(User, null=True, on_delete=models.SET_NULL)
    contact_info: models.CharField = models.CharField(
        max_length=100, blank=True, null=True
    )
    address: models.CharField = models.CharField(max_length=100, blank=True, null=True)

    # Media
    profile_image: models.ImageField = models.ImageField(
        upload_to=profile_image_path, default="default.png"
    )

    # Date Fields
    date_of_birth: models.DateField = models.DateField(
        null=True, blank=True, editable=True
    )
    age: models.IntegerField = models.IntegerField(null=True, blank=True)
    created_at: models.DateTimeField = models.DateTimeField(
        auto_now_add=True, null=True, blank=True, editable=False
    )
    updatedAt: models.DateTimeField = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["user__first_name", "created_at"]

    def __str__(self) -> str:
        user: str = self.user.username if self.user else "None"
        return f"{user}"

    @property
    def set_age(self) -> None:
        """Property to set the age of the patient numerically"""
        if self.date_of_birth:
            today = date.today()
            self.age = (
                today.year
                - self.date_of_birth.year
                - (
                    (today.month, today.day)
                    < (self.date_of_birth.month, self.date_of_birth.day)
                )
            )

        return None



# Delete image function
def delete_profile_image_and_folder(instance) -> None:
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

# Detele user instance
def deleteUserInstance(instance: Patient) -> None:
    """ Function used to delete the user instance of the patient"""
    instance.user.delete()

@receiver(pre_delete, sender=Patient)
def deletePatient(sender, instance, using, **kwargs) -> None:
    """
    Function used to delete profile image upon deletion of the profile.
    """
    # Delete User instance
    deleteUserInstance(instance)
    # Delete directory
    delete_profile_image_and_folder(instance)