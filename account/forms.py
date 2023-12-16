from django import forms
from django.contrib.auth import get_user_model
from .models import Profile

User = get_user_model()


class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "email",
            "password",
            "password_2",
            "staff_id",
        ]

    def clean_email(self):
        "Verify email is available"

        email = self.cleaned_data.get("email")
        qs = User.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError("This email already exists")
        return email

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

    def clean(self):
        """
        Verify both passwords match.
        """
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_2 = cleaned_data.get("password_2")

        if password is not None and password != password_2:
            raise forms.ValidationError("Your passwords must match")
        else:
            return cleaned_data


class ProfileRegForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = (
            "id",
            
            "phone_number",
            "address",
        )

class ProfileUpdateForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = (
            "phone_number",
            "address",
        )


class LoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.TextInput(attrs={"placeholder": "Email", "class": "form-control"})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"placeholder": "Password", "class": "form-control"}
        )
    )
