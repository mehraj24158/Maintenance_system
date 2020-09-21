from django.urls import include, path
from user import views

app_name = "user"

urlpatterns = [
    path('', views.index, name='index'),
    path('login_view', views.login_view, name='login_view'),
    # path('logout', views.logout, name='logout'),
    path('register', views.register, name='register'),
]