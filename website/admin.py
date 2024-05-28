from django.contrib import admin
from .models import Client ,  Fournisseur, Produit, BonCommande, Commande, userstatus


admin.site.register(Client)
admin.site.register(Commande)
admin.site.register(Fournisseur)
admin.site.register(Produit)
admin.site.register(BonCommande)
admin.site.register(userstatus)