from django.urls import path
from . import views

urlpatterns = [
    path('', views.User , name="User"), 
    path('home', views.home , name="home"), 
    path('File',views.File, name="File"),
    path('login_view',views.login_view, name="login_view"),
    path('logout_view', views.logout_view, name='logout_view'),
    path('save_data', views.save_data, name='save_data'),
    path('bon_commande', views.bon_commande, name='bon_commande'),
    path('commandedetails', views.commandedetails, name='commandedetails'),
    

]
