from django.db import models

class Client(models.Model):
    name = models.CharField(max_length=30)
    address = models.CharField(max_length=100)
    mail = models.EmailField(max_length=254)
    phone = models.CharField(max_length=15)
    fax = models.CharField(max_length=15)
    tax_id = models.CharField(max_length=50)

class Fournisseur(models.Model):
    identificateur=models.CharField(max_length=100, null=True)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    sujet = models.TextField(max_length=5000)
    consultation=models.CharField( max_length=50,null=True)

class Produit(models.Model):
    name = models.CharField(max_length=20)
    characteristic = models.TextField(max_length=5000)

class BonCommande(models.Model):
    numero=models.CharField( max_length=10, null=True)
    date = models.CharField(max_length=15)
    fournisseur = models.ForeignKey('Fournisseur', on_delete=models.CASCADE)
    id_commande = models.ForeignKey('Commande', on_delete=models.CASCADE)

class Commande(models.Model):
    quantity=models.CharField(max_length=5, null= True)
    unity = models.CharField(max_length=10)
    price_indiv = models.CharField(max_length=50)
    price_total = models.CharField(max_length=50)
    sum = models.CharField(max_length=50)
    id_produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
