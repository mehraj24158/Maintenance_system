from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(request):
    return render(request, "user/index.html")
def login(request):
    return HttpResponse("Welcome to the login page")
def register(request):
    return HttpResponse("Welcome to the register page")