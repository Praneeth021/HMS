from django.shortcuts import render

# Create your views here.

def HomePage(request):
    return render(request,'index.html')


def Register(request):
    return render(request,'Register.html')