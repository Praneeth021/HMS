from django.urls import path
from django.conf.urls import include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('',views.HomePage,name='HomePage'),
    path('register/',views.Register,name='Register'),
    path('register/patient_signup',views.patient_signup,name='patient_signup'),
    path('register/doctor_signup',views.doctor_signup,name='doctor_signup'),
    path('Login/',auth_views.LoginView.as_view(template_name='Login.html'),name='Login'),
    path('Logout',auth_views.LogoutView.as_view(),name='Logout'),
    path('Patient_Profile/',views.Patient_Profile,name='Patient_Profile'),
    path('Patient_Profile/<int:pk>',views.ProfileUpdate.as_view(),name='ProfileUpdate'),
    path('Doctor_Profile/',views.Doctor_Profile,name='Doctor_Profile'),
    path('Complaints/',views.ComplaintListView,name='ComplaintListView'),
    path('Invoices&Payments/',views.Invoices_And_Payments,name='Invoices_And_Payments'),
    path('Patient_Appointment/',views.Patient_Appointment,name='Patient_Appointment'),
    path('Complaints/Complaint_Registration/',views.ComplaintRegistration,name='ComplaintRegistration'),
    path('Complaints/<int:id>/',views.ComplaintDetailView,name='ComplaintDetailView'),
    path('Prescription/',views.Prescription,name='Prescription')

]