from django.shortcuts import render,redirect
from django.contrib import messages
from .forms import UserRegisterForm,DoctorRegisterForm,ProfileUpdateForm,ComplaintRegisterForm
from .models import Users,Patient,Doctor,Complaint
from django.contrib.auth.decorators import login_required

# Create your views here.

def HomePage(request):
    return render(request,'index.html')


def Register(request):
    return render(request,'Register.html')


def doctor_signup(request):
    if request.method=='POST':
        userform=UserRegisterForm(request.POST,request.FILES,prefix='userform')
        doctorform=DoctorRegisterForm(request.POST,request.FILES,prefix='doctorform')
        if userform.is_valid() and doctorform.is_valid():
                user = userform.save(commit=False)
                user.role = Users.DOCTOR
                user.save()
                doctor=doctorform.save(commit=False)
                doctor.user=user
                doctor.save()
                username=userform.cleaned_data.get('username')
                messages.success(request,f'Account created for {username}')
                return redirect('Login')
        else:
            print(userform.errors)
    else:
        userform = UserRegisterForm(prefix='userform')
        doctorform=DoctorRegisterForm(prefix='doctorform')
        context={'form': userform,'dform':doctorform}
        return render(request,'Doctor_Signup.html',context)


def patient_signup(request):
    doctors=Doctor.objects.all()
    if request.method=='POST':
        userform=UserRegisterForm(request.POST,prefix='userform')
        if userform.is_valid():
            user = userform.save()
            user.role = Users.PATIENT
            user.save()
            patient = Patient(user=user)
            patient.save()
            username = userform.cleaned_data.get('username')
            messages.success(request,f'Account created for {username}')
            return redirect('Login')
    else:
        userform = UserRegisterForm(prefix='userform')
        # patientform = PatientSignupForm(request.POST, prefix='patientform')
        return render(request=request, template_name='Patient_Signup.html',context={'form': userform,'doctors':doctors})



def Patient_Profile(request):
    return render(request,'Patient_Profile.html')


def Doctor_Profile(request):
    return render(request,'Doctor_Profile.html')


def Profile_Update(request):
    if request.method=='POST':
        updateform=ProfileUpdateForm(request.POST,prefix='userform')
        if updateform.is_valid:
            user=request.user


@login_required
def ComplaintRegistration(request):
    if request.method =='POST':
        complaintform=ComplaintRegisterForm(request.POST,prefix='complaintform')
        if complaintform.is_valid():
            complaint=complaintform.save(commit=False)
            complaint.patient=Patient.objects.get(user=request.user)
            user1=Users.objects.get(username=request.POST.get('Doctor'))
            doctor=Doctor.objects.get(user=user1)
            complaint.Doctor=doctor
            complaint.save()
            messages.success(request,f'Complaint Registered')
            return redirect('HomePage')
    else:
        Doctors=Doctor.objects.all()
        complaintform=ComplaintRegisterForm(prefix='complaintform')
        return render(request,'ComplaintRegistration.html',{'complaintform':complaintform,'Doctors':Doctors})

@login_required
def ComplaintListView(request):
    patient=Patient.objects.get(user=request.user)
    complaints=Complaint.objects.filter(patient=patient).values()
    template_name='ComplaintView.html'
    return render(request,template_name,context={'complaints':complaints})

@login_required
def ComplaintDetailView(request,id):
    complaint=Complaint.objects.get(id=id)
    return render(request,'ComplaintDetail.html',{'complaint':complaint})

@login_required
def DoctorComplaintDetailView(request,id):
    complaint=Complaint.objects.get(id=id)
    return render(request,'DoctorComplaintDetailView.html',{'complaint':complaint})


@login_required
def PrescriptionForm(request,primary_key):
    return render(request,'PrescriptionForm.html',{'primary_key':primary_key})

@login_required
def Invoices_And_Payments(request):
    return render(request,'Invoice_And_Payments.html')

@login_required
def Patient_Appointment(request):
    return render(request,'Patient_Appointment.html')
    