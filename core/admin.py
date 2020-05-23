from django.contrib import admin

# Register your models here.
from .models import Users,Patient,Doctor,HR,Receptionist

admin.site.register(Users)
admin.site.register(Patient)
admin.site.register(Doctor)
admin.site.register(HR)
admin.site.register(Receptionist)
