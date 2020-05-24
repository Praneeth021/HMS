from django.shortcuts import render,redirect,reverse
from django.contrib import messages
from .forms import UserRegisterForm,DoctorRegisterForm,ComplaintRegisterForm
from .models import Users,Patient,Doctor,Complaint,Appointment,Receptionist
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import DeleteView

# Create your views here.

class ProfileDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model= Patient
    success_url='/'
    template_name='confirm_delete.html'

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
    pending=
    return render(request,'receiptionist.html',{'patient':patient,'appointment':appointment})


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
    

class PatientUpdate(UpdateView):
    model=Users
    fields=['first_name','last_name','email','username','password','age','gender','phoneno','address']
    template_name='Patient_Profile.html'
    


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
def Prescription(request):
    user=request.user
    doctor=Doctor.objects.get(user=user)
    complaint=Complaint.objects.filter(Doctor=doctor).values()
    return render(request,'DoctorComplaintView.html',{'complaints':complaint})





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
