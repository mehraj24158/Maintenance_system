from django.urls import include, path
from user import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login, name='login'),
    path('login', views.logout, name='logout'),
    path('register', views.register, name='register'),
]