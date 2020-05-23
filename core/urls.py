from django.urls import path
from django.conf.urls import include
from . import views

urlpatterns = [
    path('',views.HomePage,name='Home'),
    path('register/',views.Register,name='Register'),
]