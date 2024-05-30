from django.urls import path
from . import views

urlpatterns = [
    path('', views.user , name="user"), 
    path('home', views.home , name="home"), 
    path('File',views.File, name="File"),
    path('login_view',views.login_view, name="login_view"),
    path('logout_view', views.logout_view, name='logout_view'),
    path('save_data', views.save_data, name='save_data'),
    path('bon_commande', views.bon_commande, name='bon_commande'),
    path('commandedetails', views.commandedetails, name='commandedetails'),
    path('inscription', views.inscription, name='inscription'),
    path('deletecommande', views.deletecommande, name='deletecommande'),
    path('gestionf', views.gestionf, name='gestionf'),
    path('Fcommande', views.Fcommande, name='Fcommande'),
    path('deletecf', views.deletecf, name='deletecf'),
    path('deletef', views.deletef, name='deletef'),
    path('userinterface', views.userinterface, name='userinterface'),
    path('activate_user', views.activate_user, name='activate_user'),
    path('deleteuser', views.deleteuser, name='deleteuser'),
    path('edit/<str:item_type>/<int:item_id>/', views.edit_item, name='edit_item'),
    

]
