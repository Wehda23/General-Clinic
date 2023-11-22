from django.db import models
import uuid

# Create your models here.

"""sql
CREATE TABLE Patient (
    Patient_ID UUID PRIMARY KEY,
    First_Name VARCHAR(50),
    Last_Name VARCHAR(50),
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
    first_name: models.CharField = models.CharField(
        max_length=50, blank=False, null=False
    )
    last_name: models.CharField = models.CharField(
        max_length=50, blank=False, null=False
    )
    email_address: models.EmailField = models.EmailField(max_length=255, default ="")
    contact_info: models.CharField = models.CharField(
        max_length=100, blank=True, null=True
    )
    address: models.CharField = models.CharField(max_length=100, blank=True, null=True)

    # Date Fields
    date_of_birth: models.DateField = models.DateField(
        null=False, blank=False, editable=True
    )
    created_at: models.DateTimeField = models.DateTimeField(
        auto_now_add=True, null=True, blank=True, editable=False
    )
    updatedAt: models.DateTimeField = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["first_name", "created_at"]

    def __str__(self) -> str:
        return self.first_name
