from django.urls import path
from .views import *
from django.contrib.auth.views import (
    LogoutView,
    PasswordResetConfirmView,
    PasswordResetDoneView,
    PasswordResetCompleteView,
    PasswordResetView,
)

app_name = "account"

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path(
        "register/health-worker/", RegisterHealthWorkerView.as_view(), name="register"
    ),
    path("register/patient/", RegisterUser.as_view(), name="patient_registration"),

    path("profile-update/", ProfileUpdateView.as_view(), name="profile_update"),

    path("logout/", LogoutView.as_view(), name="logout"),
]
