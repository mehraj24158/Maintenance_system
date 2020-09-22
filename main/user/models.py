from django.db import models
from enum import Enum

class Status(Enum):
    """
    Enum class containing the status of a ticket
    """
    active = 1
    assigned = 2
    completed = 3

class User(models.Model):
    """
    Abstract user class implementing base functionality
    """
    username = models.CharField(max_length=64)
    f_name = models.CharField(max_length=64)
    l_name = models.CharField(max_length=64)
    phone_number = models.CharField(max_length=10)
    email = models.EmailField()
    password = models.CharField(max_length=64)

    class Meta:
        abstract = True

class Resident(User):
    """
    Resident class containing resident specific information
    """
    house_number = models.IntegerField()

class Technician(User):
    """
    Technician class containing technician specific information
    """
    date_hired = models.DateField()

class Appointment(models.Model):
    """
    Appointment class containing appointment information
    """
    date = models.DateTimeField
    tech_confirm = False
    res_confirm = False

    def confirm():
        if tech_confirm == True and res_confirm == True:
            return True
        else:
            return False

class Ticket(models.Model):
    """
    Ticket class containing ticket specific information
    """
    technician = models.ForeignKey(Technician, on_delete=models.PROTECT)
    resident = models.ForeignKey(Resident, on_delete=models.PROTECT)
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    description = models.CharField(max_length=280)
    date_created = models.DateField()
    date_completed = models.DateField()
    status = Status.active

    def create_appointment():
        pass
        #self.appointment = Appointment
