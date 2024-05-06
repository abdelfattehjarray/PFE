from django.urls import path
from . import views

urlpatterns = [
    path('', views.home , name="home"), 
    path('User',views.User, name="User"),
    path('File',views.File, name="File"),
    

]
