from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import DetailView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.contrib.auth import login, authenticate, logout, get_user_model
from django.contrib import messages
from .forms import LoginForm, UserRegisterForm, ProfileRegForm, ProfileUpdateForm


def return_errors(a, b):
    array = [a, b]
    result = []
    for i in array:
        if i:
            result.append(i)
    return result


class LoginView(View):
    template_name = "login.html"
    form_class = LoginForm

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=email, password=password)

            if user is not None:
                login(request, user)
                return redirect("record:index")
            else:
                messages.error(request, "Invalid email or password")

        return render(request, self.template_name, {"form": form})


class RegisterHealthWorkerView(View):
    template_name = "signup.html"

    def get(self, request):
        user_form = UserRegisterForm()
        profile_form = ProfileRegForm()
        return render(
            request,
            self.template_name,
            {"user_form": user_form, "profile_form": profile_form},
        )

    @transaction.atomic
    def post(self, request):
        user_form = UserRegisterForm(request.POST)
        profile_form = ProfileRegForm(request.POST)
        print(user_form, profile_form)

        if user_form.is_valid():
            print(user_form, "is_valid")
            if profile_form.is_valid():
                print(profile_form)
                user = user_form.save(commit=False)
                user.is_active = True
                user.is_healthworker = True
                profile = profile_form.save(commit=False)
                profile.user = user

                user.save()
                profile.save()
                print("saved successfully")

                # register_mail_confirmation(account=user)

                login(request, user)
                messages.success(request, "Registration successful.")
                return redirect("record:index")
        data = return_errors(user_form.errors, profile_form.errors)
        messages.error(request, data)
        return redirect("account:register")


class RegisterUser(View):
    template_name = "patient_signup.html"

    def get(self, request):
        user_form = UserRegisterForm()
        profile_form = ProfileRegForm()
        return render(
            request,
            self.template_name,
            {"user_form": user_form, "profile_form": profile_form},
        )

    @transaction.atomic
    def post(self, request):
        user_form = UserRegisterForm(request.POST)
        profile_form = ProfileRegForm(request.POST)
        print(user_form, profile_form)

        if user_form.is_valid():
            print(user_form, "is_valid")
            if profile_form.is_valid():
                print(profile_form)
                user = user_form.save(commit=False)
                user.is_active = True
                user.is_patient = True
                profile = profile_form.save(commit=False)
                profile.user = user

                user.save()
                profile.save()
                print("saved successfully")

                # register_mail_confirmation(account=user)

                login(request, user)
                messages.success(request, "Registration successful.")
                return redirect("record:index")
        data = return_errors(user_form.errors, profile_form.errors)
        messages.error(request, data)
        return redirect("account:patient_registration")
    
    
class ProfileUpdateView(View):
    template_name = "profile.html"

    def get(self, request):
        profile_form = ProfileUpdateForm()
        user_form = UserRegisterForm()
        
        return render(
            request,
            self.template_name,
            {"user_form":user_form, "profile_form": profile_form},
        )
    
    @transaction.atomic
    def post(self, request):
        profile_form = ProfileUpdateForm(request.POST)

        
        if profile_form.is_valid():
            
            profile = profile_form.save(commit=False)
            profile.user = request.user
           
            profile.save()
            print("saved successfully")

            # register_mail_confirmation(account=user)

            messages.success(request, "Profile updated")
            return redirect("record:index")
        messages.error(request, profile_form.errors)
        return redirect("account:profile_update")
    
