from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View, ListView
from django.contrib.auth import get_user_model
from django.db.models import Avg
from account.models import Profile
from .models import MedicalData
from datetime import datetime
from .permissions import is_healthworker
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test
from .forms import MedicalDataForm



# Create your views here.

User = get_user_model()


class IndexView(LoginRequiredMixin, View):
    template_name = "index.html"

    def get(self, request, *args, **kwargs):
        number_of_patient = User.objects.filter(is_patient=True).count()

        print(number_of_patient)

        number_of_health_worker = User.objects.filter(is_healthworker=True).count()

        profiles_with_medical_data = Profile.objects.filter(data_profile__isnull=False)

        # Calculate average BMI
        average_bmi = round(profiles_with_medical_data.aggregate(avg_bmi=Avg('data_profile__bmi'))['avg_bmi'])
        

        now = datetime.now().date()
        total_age = 0
        count = 0

        for profile in profiles_with_medical_data:
            medical_data = MedicalData.objects.filter(profile=profile).first()
            if medical_data and medical_data.dob:
                age = now.year - medical_data.dob.year
                total_age += age
                count += 1

        # Avoid division by zero
        average_age = round(total_age / count if count > 0 else 0)

        medical_data_with_diagnoses = MedicalData.objects.exclude(diagnosis__isnull=True)

        # Create a dictionary to store disease counts
        disease_count_dict = {}

      
        for medical_data in medical_data_with_diagnoses:
            disease = medical_data.diagnosis
            if disease in disease_count_dict:
                disease_count_dict[disease] += 1
            else:
                disease_count_dict[disease] = 1


        medical_data_with_blood_types = MedicalData.objects.exclude(blood_group__isnull=True)

        # Create a dictionary to store blood type counts
        blood_type_count_dict = {}

        # Count the occurrences of each blood type
        for medical_data in medical_data_with_blood_types:
            blood_type = medical_data.blood_group
            if blood_type in blood_type_count_dict:
                blood_type_count_dict[blood_type] += 1
            else:
                blood_type_count_dict[blood_type] = 1
      

        context = {
            "total_patient": number_of_patient,
            "total_health_worker": number_of_health_worker,
            "average_bmi": average_bmi,
            "average_age":average_age,
            "disease_count_dict":disease_count_dict,
            "blood_type_count_dict":blood_type_count_dict,
        }
        return render(request, self.template_name, context)


class UserMedicalRecordsView(LoginRequiredMixin, ListView):
    template_name = 'medical_records.html'
    model = Profile
    context_object_name = 'profiles_with_medical_data'

    @method_decorator(user_passes_test(is_healthworker))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_queryset(self):
        # Fetch all profiles with associated medical data
        return Profile.objects.filter(data_profile__isnull=False)
    


class DetailRecordView(LoginRequiredMixin, View):
    template_name = "medical_record.html"

    @method_decorator(user_passes_test(is_healthworker))
    def get(self, request, *args, **kwargs):
        user = User.objects.get(id=kwargs["id"])
        profile = Profile.objects.get(user=user)

        context = {
            "user": user,
            "profile":profile
            }
        
        return render(request, self.template_name, context)
    
class MyRecordView(LoginRequiredMixin, View):
    template_name = "medical_record.html"

    def get(self, request, *args, **kwargs):
        user = User.objects.get(id=request.user.id)
        profile = Profile.objects.get(user=user)

        context = {
            "user": user,
            "profile":profile
            }
        
        return render(request, self.template_name, context)
    
class DataUpdateView(View):
    template_name = "medical_data_update.html"

    def get(self, request, *args, **kwargs):
        user = User.objects.get(id=request.user.id)
        profile = Profile.objects.get(user=user)
        medical_data, created = MedicalData.objects.get_or_create(profile=profile)

        # Populate the form with the existing data
        form = MedicalDataForm(instance=medical_data)

        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        user = User.objects.get(id=request.user.id)
        profile = Profile.objects.get(user=user)        
        medical_data, created = MedicalData.objects.get_or_create(profile=profile)

        # Populate the form with the submitted data
        form = MedicalDataForm(request.POST, instance=medical_data)

        if form.is_valid():
            form.save()
            return redirect("record:my_record")  # Redirect to the same page after successful submission

        return render(request, self.template_name, {"form": form})
