# Generated by Django 4.2.8 on 2023-12-16 11:58

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="MedicalData",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "dob",
                    models.DateField(blank=True, help_text="Date of birth", null=True),
                ),
                (
                    "bmi",
                    models.PositiveSmallIntegerField(
                        blank=True, help_text="Body Mass Index", null=True
                    ),
                ),
                ("blood_group", models.CharField(blank=True, max_length=10, null=True)),
                ("allergy", models.TextField(blank=True)),
                ("medication", models.TextField(blank=True)),
                ("diagnosis", models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
    ]
