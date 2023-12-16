from django.db import models
from django.utils.translation import gettext_lazy as _
from account.models import Profile

# Create your models here.

class MedicalData(models.Model):

    profile = models.OneToOneField(Profile, related_name="data_profile" ,on_delete=models.CASCADE, null=True)

    dob = models.DateField(blank=True, null=True, help_text=_("Date of birth"))

    bmi = models.PositiveSmallIntegerField(
        null=True, blank=True, help_text=_("Body Mass Index")
    )

    blood_group = models.CharField(max_length=10, blank=True, null=True)

    allergy = models.TextField(blank=True)

    medication = models.TextField(blank=True)

    diagnosis = models.CharField(max_length=100, blank=True, null=True)