from django.db import models
from django.contrib.auth.models import User
from datetime import date
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
    user: User = models.OneToOneField(User, null=True, on_delete=models.SET_NULL)
    contact_info: models.CharField = models.CharField(
        max_length=100, blank=True, null=True
    )
    address: models.CharField = models.CharField(max_length=100, blank=True, null=True)

    # Date Fields
    date_of_birth: models.DateField = models.DateField(
        null=False, blank=False, editable=True
    )
    age: models.IntegerField = models.IntegerField(null=True, blank=True)
    created_at: models.DateTimeField = models.DateTimeField(
        auto_now_add=True, null=True, blank=True, editable=False
    )
    updatedAt: models.DateTimeField = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["user__first_name", "created_at"]

    def __str__(self) -> str:
        return self.user.first_name

    @property
    def set_age(self):
        
        if self.date_of_birth:
            today = date.today()
            self.age = today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))
            
        return None
    
    def save(self):
        self.set_age
        super().save()