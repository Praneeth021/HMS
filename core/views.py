from django.shortcuts import render,redirect,reverse
from django.contrib import messages
from .forms import UserRegisterForm,DoctorRegisterForm,ComplaintRegisterForm,DoctorUpdateForm,AppointmentForm
from .models import Users,Patient,Doctor,Complaint,Appointment,Prescription,Invoices
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import UpdateView


from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import DeleteView

# Create your views here.

@login_required
def updatePatientForm(request,id):

	patient = Patient.objects.get(user_id=id)
	form = UserRegisterForm(instance=patient)

	if request.method == 'POST':
		form = UserRegisterForm(request.POST, instance=patient)
		if form.is_valid():
			form.save()
			return redirect('Patient_Profile')

	context = {'form':form}
	return render(request, 'Patient_Signup.html', context)



def deleteProfile(request, pk):
	profile = Patient.objects.get(id=pk)
	if request.method == "POST":
		profile.delete()
		return redirect('/')

	context = {'profile':profile}
	return render(request, 'confirm_delete.html', context)


def HomePage(request):
    return render(request,'index.html')


def Register(request):
    return render(request,'Register.html')

def Receiptionist(request):
    patient=Patient.objects.all()
    appointment=Appointment.objects.all()
    total_appointment=appointment.count()
    pending=appointment.filter(status='Pending').count()
    completed=appointment.filter(status='Completed').count()
    context={
        'total_appointment':total_appointment,
        'pending':pending,
        'completed':completed,
        'patient':patient,'appointment':appointment

    }
    return render(request,'receiptionist.html',context=context)


def CreatePatient(request):
   
    if(request.method== 'POST'): 
        form= UserRegisterForm(request.POST)
        if form.is_valid():
            user=form.save()
            user.role = Users.PATIENT
            user.save()
            patient = Patient(user=user)
            patient.save()
            username= form.cleaned_data.get('username')
            messages.success(request, f'Created a patient')
            return redirect('Receiptionist')
            
    else:    
         form= UserRegisterForm()
    return render(request, 'Patient_signup.html', {'form': form,'patient':patient})


def deletePatient(request,id):
    patient = Patient.objects.get(user_id=id)
    if request.method == "POST":
        patient.delete()
        return redirect('Receiptionist')

    context = {'d':patient}
    return render(request, 'PatientDelete.html', context)

def CreateAppointment(request):
   
    if(request.method== 'POST'): 
        form= AppointmentForm(request.POST)
        if form.is_valid():
            user=form.save()
            username= form.cleaned_data.get('username')
            messages.success(request, f'Created a Appointment')
            return redirect('Receiptionist')
            
    else:    
         form= AppointmentForm()
    return render(request, 'create_appointment.html', {'form': form})
    
   



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


@login_required
def Patient_Profile(request):
    return render(request,'Patient_Profile.html')

@login_required
def Doctor_Profile(request):
    return render(request,'Doctor_Profile.html')



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
    complaints=Complaint.objects.filter(patient=patient)
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
    patient=Patient.objects.get(user=request.user)
    invoice=Invoices.objects.filter(patient=patient)
    return render(request,'Invoice_And_Payments.html',{'invoice':invoice})

@login_required
def Patient_Appointment(request):
    user=request.user
    patient=Patient.objects.get(user_id=user.id)
    appointments=Appointment.objects.filter(patient=patient)
    return render(request,'Patient_Appointment.html',{'Appointments':appointments})
    

@login_required
def DoctorComplaintView(request):
    user=request.user
    doctor=Doctor.objects.get(user=user)
    complaint=Complaint.objects.filter(Doctor=doctor)
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
    appointments=Appointment.objects.filter(doctor=doctor)
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
    invoices=Invoices.objects.all()
    return render(request,'Accounting.html',{'invoice':invoices})



def CreateReceptionist(request):
   
    if(request.method== 'POST'): 
        form= UserRegisterForm(request.POST)
        if form.is_valid():
            user=form.save()
            user.role = Users.RECEPTIONIST
            user.save()
            receptioinist = Receptionist(user=user)
            receptioinist.save()
            username= form.cleaned_data.get('username')
            messages.success(request, f'Created a patient')
            return redirect('Receiptionist')
            
    else:    
         form= UserRegisterForm()
    return render(request, 'Patient_signup.html', {'form': form,})




def Invoicess(request,id):
    invoice=Invoices.objects.get(id=id)
    return render(request,'invoice.html',{'i':invoice})