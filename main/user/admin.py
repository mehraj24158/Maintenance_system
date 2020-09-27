from django.contrib import admin

from .models import Resident, Technician, Ticket, Appointment
# Register your models here.
admin.site.register(Resident)
admin.site.register(Technician)
admin.site.register(Ticket)
admin.site.register(Appointment)

