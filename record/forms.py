from django import forms
from django.contrib.auth import get_user_model
from .models import MedicalData

User = get_user_model()


class MedicalDataForm(forms.ModelForm):
    BLOOD_TYPE_CHOICES = [
        ("A+", "A+"),
        ("A-", "A-"),
        ("B+", "B+"),
        ("B-", "B-"),
        ("AB+", "AB+"),
        ("AB-", "AB-"),
        ("O+", "O+"),
        ("O-", "O-"),
    ]

    blood_type = forms.ChoiceField(choices=BLOOD_TYPE_CHOICES, required=False)
    diagnosis = forms.CharField(max_length=100, required=False)

    class Meta:
        model = MedicalData
        fields = ["profile", "dob", "blood_type", "bmi", "allergy", "medication", "diagnosis"]
