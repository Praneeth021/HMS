from django.shortcuts import render,redirect,reverse
from django.contrib import messages
from .forms import UserRegisterForm,DoctorRegisterForm,ComplaintRegisterForm,DoctorUpdateForm
from .models import Users,Patient,Doctor,Complaint,Appointment,Prescription
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import UpdateView

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


class ProfileUpdate(UpdateView):
    model=Users
    fields=['first_name','last_name','email','username','password','age','gender','phoneno','address']
    template_name='Patient_Signup.html'
    def get_absolute_url(self):
        return reverse('Patient_Profile', kwargs={'pk': self.pk})


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
            return redirect('ComplaintListView')
    else:
        Doctors=Doctor.objects.all()
        complaintform=ComplaintRegisterForm(prefix='complaintform')
        return render(request,'Complaint_Registration.html',{'complaintform':complaintform,'Doctors':Doctors})

@login_required
def ComplaintListView(request):
    patient=Patient.objects.get(user=request.user)
    complaints=Complaint.objects.filter(patient=patient).values()
    template_name='Medical_History.html'
    return render(request,template_name,context={'complaints':complaints})

@login_required
def ComplaintDetailView(request,id):
    complaint=Complaint.objects.get(id=id)
    return render(request,'Complaint_DetailView.html',{'complaint':complaint})

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
    user=request.user
    patient=Patient.objects.get(user_id=user.id)
    appointments=Appointment.objects.get(patient=patient)
    return render(request,'Patient_Appointment.html',{'Appointments':appointments})
    

@login_required
def DoctorComplaintView(request):
    user=request.user
    doctor=Doctor.objects.get(user=user)
    complaint=Complaint.objects.filter(Doctor=doctor).values()
    return render(request,'DoctorComplaintView.html',{'complaints':complaint})



def AdvicePrescription(request,id):
    if request.method == 'POST':
        Description=request.POST.get('Description')
        Description.capitalize()
        complaint=Complaint.objects.get(id=id)
        patient=complaint.patient
        doctor=complaint.Doctor
        prescription=Prescription(Doctor=doctor,patient=patient)
        prescription.Description=Description
        prescription.complaint=complaint
        prescription.save()
        return redirect('Prescription')
    return render(request,'Prescription_Form.html')




def DoctorAppointments(request):
    doctor=Doctor.objects.get(user=request.user)
    appointments=Appointment.objects.filter(doctor=doctor).values()
    return render(request,'Doctor_Appointments.html',{'appointments':appointments})





def hr_dashboard(request):
    doctors = Doctor.objects.all()
    patients = Patient.objects.all()
    total_patients = patients.count()
    total_doctors = doctors.count()
    onduty_doctors = doctors.filter(status='onduty').count()

    context = {'total_doctors':total_doctors,
    'total_patients':total_patients,
    'onduty_doctors':onduty_doctors,'doctors':doctors }

    return render(request, 'Hr_Dashboard.html', context)


def updateDoctorForm(request, id):

	doctor = Doctor.objects.get(user_id=id)
	form = DoctorUpdateForm(instance=doctor)

	if request.method == 'POST':
		form = DoctorUpdateForm(request.POST, instance=doctor)
		if form.is_valid():
			form.save()
			return redirect('Hr_Dashboard')

	context = {'form':form}
	return render(request, 'DoctorUpdateForm.html', context)


def deleteDoctor(request,id):
    doctor = Doctor.objects.get(user_id=id)
    if request.method == "POST":
        doctor.delete()
        return redirect('Hr_Dashboard')

    context = {'d':doctor}
    return render(request, 'DoctorDelete.html', context)



def Accounting(request):
    return render(request,'Accounting.html')
