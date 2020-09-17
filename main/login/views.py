from django.http import HttpResponse


def index(request):
    return HttpResponse("Welcome to the index")

def hello(request):
    return HttpResponse("Hello world.")

def bye(request):
    return HttpResponse("Good bye world")

def greet(request, name):
    return HttpResponse(f"Greetings mon {name.capitalize()}!")

