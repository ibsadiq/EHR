# Generated by Django 4.2.8 on 2023-12-16 09:19

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("account", "0003_profile_allergies_profile_blood_group_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="profile",
            old_name="allergies",
            new_name="allerg",
        ),
        migrations.RenameField(
            model_name="profile",
            old_name="medications",
            new_name="medication",
        ),
        migrations.AddField(
            model_name="profile",
            name="bmi",
            field=models.PositiveSmallIntegerField(
                blank=True, help_text="Body Mass Index", null=True
            ),
        ),
    ]