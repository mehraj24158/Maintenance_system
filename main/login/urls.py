from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('hello', views.hello),
    path('bye', views.bye),
    path("<str:name>", views.greet),
]

