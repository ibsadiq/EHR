from django.db import models
from django.db.models.deletion import CASCADE, SET_NULL
from django.core.validators import RegexValidator
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)

from django.utils.translation import gettext_lazy as _
import random


class UserManager(BaseUserManager):
    def create_user(
        self,
        email,
        password=None,
        **extra_fields
    ):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


    def create_superuser(self, email, password=None, **extra_fields):
        "Creates and saves a superuser with a the given email and password"
        user = self.create_user(
            email,
            password=password,
        )
        user.is_superuser = True
        user.is_staff = True
        user.is_active = True
        user.save(using=self._db)

        profile = Profile()
        profile.user = user
        profile.save()
        return user

    # def get_users_with_bmi(self):
    #     return self.filter(profile_user__bmi__isnull=False)


class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(
        max_length=100,
    )

    last_name = models.CharField(
        max_length=100,
    )

    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    staff_id = models.CharField(max_length=8, null=True, blank=True)

    date_joined = models.DateTimeField(auto_now_add=True)

    last_login = models.DateTimeField(verbose_name="last login", auto_now=True)

    is_active = models.BooleanField(default=False)

    is_staff = models.BooleanField(default=False)

    is_superuser = models.BooleanField(default=False)

    # custom fields to be used for our user classification
    is_patient = models.BooleanField(default=False)

    is_healthworker = models.BooleanField(default=False)

    # history = HistoricalRecords()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []  # email & Password are required by default.
    READONLY_FIELDS = ["date_joined", "last_login"]

    objects = UserManager()

    def __str__(self):
        return self.email

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def isSuperUser(self):
        "Is the user a super user?"
        return self.is_superuser

    @classmethod
    def get_user(cls, email):
        return cls.objects.get(email=email)


class Profile(models.Model):
    

    phone_number_regex = RegexValidator(regex=r"^\+?1?\d{8,15}$")

    user = models.OneToOneField(
        User, related_name="profile_user", on_delete=models.CASCADE, null=True
    )

    profile_id = models.SlugField(
        blank=True, null=True, help_text=_("Unique identifier for the profile")
    )

    phone_number = models.CharField(
        validators=[phone_number_regex], max_length=16, unique=True
    )

    address = models.CharField(
        max_length=255, blank=True, null=True, help_text=_("Address of the user.")
    )

    


    def save(self, *args, **kwargs):
        self.profile_id = (
            f"{self.user.first_name}-{self.user.last_name}{random.randint(1, 5000)}"
        )
        super(Profile, self).save(*args, **kwargs)
