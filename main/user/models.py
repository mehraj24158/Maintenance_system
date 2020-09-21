from django.db import models
from enum import Enum, auto

class Status(Enum):
    active = 1
    assigned = 2
    completed = 3

class User(models.Model):
    username = models.CharField(max_length=64)
    f_name = models.CharField(max_length=64)
    l_name = models.CharField(max_length=64)
    phone_number = models.CharField(max_length=64)
    password = models.CharField(max_length=64)

class Resident(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)

class Technician(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)

class Ticket(models.Model):
    technician = models.ForeignKey(Technician, on_delete=models.PROTECT)
    resident = models.ForeignKey(Resident, on_delete=models.PROTECT)
    description = models.CharField(max_length=280)
    Status = Status.active

    