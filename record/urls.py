from django.urls import path
from .views import *


app_name = "record"

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path('records/', UserMedicalRecordsView.as_view(), name='medical_records'),
    path('records/<int:id>/', DetailRecordView.as_view(), name='detail'),
    path('records/myrecords', MyRecordView.as_view(), name='my_record'),
    path('records/update/', DataUpdateView.as_view(), name="record_update"),
    
    

]
