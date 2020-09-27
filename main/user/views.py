from django.shortcuts import render, reverse
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout

# Create your views here.

def index(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('user:login_view'))
    return render(request, "user/index.html")


def login_view(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('user:index'))
    else:
        return HttpResponse("else reached")

def logout_view(request):
    pass

def register(request):
    return render(request, "user/register.html")

