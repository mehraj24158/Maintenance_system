from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(request):
    return render(request, "user/index.html")


def login(request):
    return render(request, "user/login.html")

def logout(request):
    return render(request, 'user/logout.html')


def register(request):
    return render(request, "user/register.html")