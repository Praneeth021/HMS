# Create your models here.

from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db import models
from django.shortcuts import reverse


class Users(AbstractUser):
    PATIENT=1
    DOCTOR=2
    HR=3
    RECEPTIONIST=4
    ROLE_CHOICES = (
        (PATIENT, 'Patient'),
        (DOCTOR, 'Doctor'),
        (HR,'HR'),
        (RECEPTIONIST,'Receptionist')
    )
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )

    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES,null=True,blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    age=models.IntegerField(null=True,blank=True)
    phoneno=models.BigIntegerField(null=True,blank=True)
    address=models.TextField(null=True,blank=True)

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('Receiptionist')

class Doctor(models.Model):
    status_choices=(
        ('onduty','onduty'),
        ('offduty','offduty'),
    )
    user=models.OneToOneField(Users,on_delete=models.CASCADE,primary_key=True)
    Education=models.CharField(max_length=500)
    Specialization=models.CharField(max_length=500)
    AadharNo=models.IntegerField()
    Attendence=models.IntegerField(null=True,blank=True)
    Salary=models.IntegerField(null=True,blank=True)
    status=models.CharField(choices=status_choices,max_length=300)

    def __str__(self):
        return self.user.username

class Patient(models.Model):
    user=models.OneToOneField(Users,on_delete=models.CASCADE,primary_key=True)

    def __str__(self):
        return self.user.username


class Complaint(models.Model):
    Doctor=models.ForeignKey(Doctor,on_delete=models.CASCADE)
    patient=models.ForeignKey(Patient,on_delete=models.CASCADE)
    Complaint_Name=models.CharField(max_length=500)
    Symptom1=models.CharField(max_length=500)
    Symptom2=models.CharField(max_length=500)
    Description=models.TextField()
    Date=models.DateTimeField(auto_now=True)

    def _str_(self):
        return self.Complaint_Name


class Prescription(models.Model):
    complaint=models.OneToOneField(Complaint,on_delete=models.CASCADE,primary_key=True)
    patient=models.ForeignKey(Patient,on_delete=models.CASCADE)
    Doctor=models.ForeignKey(Doctor,on_delete=models.CASCADE)
    Date=models.DateTimeField(auto_now=True)
    Description=models.TextField()



class Receptionist(models.Model):
    user=models.OneToOneField(Users,on_delete=models.CASCADE,primary_key=True)



class HR(models.Model):
    user=models.OneToOneField(Users,on_delete=models.CASCADE,primary_key=True)



class Appointment(models.Model):
    status_choices=(
        ('Completed','Completed'),
        ('Pending','Pending'),
    )
    patient=models.ForeignKey(Patient,on_delete=models.CASCADE)
    doctor=models.ForeignKey(Doctor,on_delete=models.CASCADE)
    Time=models.TimeField()
    Date=models.DateField()
    status=models.CharField(choices=status_choices,max_length=300)


class Invoices(models.Model):
    patient=models.ForeignKey(Patient,on_delete=models.CASCADE)
    Total_Amount=models.IntegerField()
    Paid_Amount=models.IntegerField()
    Outstanding=models.IntegerField()
    date=models.DateField()



