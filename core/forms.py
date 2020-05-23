from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Users
from .models import Doctor,Complaint


class UserRegisterForm(UserCreationForm):
    first_name=forms.CharField(max_length=100,required=True,),
    last_name=forms.CharField(max_length=100,required=True),
    email=forms.EmailField(required=True),
    class Meta:
        model=Users
        fields=['first_name','last_name','email','username','password1','password2','age','gender','phoneno','address']


class DoctorRegisterForm(forms.ModelForm):
    class Meta:
        model=Doctor
        fields=['Education','Specialization','AadharNo']

    
class ComplaintRegisterForm(forms.ModelForm):
    class Meta:
        model=Complaint
        fields=['Complaint_Name','Symptom1','Symptom2','Description']



class PatientUpdateForm(models.ModelForm):
    class Meta:
        model=Users
        fields=['first_name','last_name','email','username','password1','password2','age','gender','phoneno','address']