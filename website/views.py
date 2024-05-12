from django.db import IntegrityError
from .models import Client, Fournisseur, BonCommande,Produit, Commande
from .extractcode import pdf, tablepdf
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.utils.datastructures import MultiValueDictKeyError



@csrf_exempt
def File(request):
    if request.method == 'POST':
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            print("Received AJAX POST request")

            data = json.loads(request.body.decode('utf-8'))
            print("Data:", data) 


            fournisseur_data = data['fournisseur']
            produit_data = data['produit']
            commande_data = data['commande']
            client_data = data['client']
            bonCommande_data = data['bonCommande']

            try:

                if not all(key in fournisseur_data for key in ['identificateur', 'name', 'adresse', 'sujet', 'consultation']):
                 return JsonResponse({'error': 'Missing data in fournisseur_data'}, status=400)
                # Save Fournisseur
                fournisseur, created = Fournisseur.objects.get_or_create(
                    identificateur=str(fournisseur_data['identificateur']),
                    defaults={
                        'name':str( fournisseur_data['name']),
                        'address': str(fournisseur_data['adresse']),
                        'sujet': str(fournisseur_data['sujet']),
                        'consultation': str(fournisseur_data['consultation'])
                    }
                )

                # Save Produit
                produit, created = Produit.objects.get_or_create(
                    name=str(produit_data['namep']),
                    characteristic=str(produit_data['characteristic'])
                )

                # Save Commande
                commande = Commande.objects.create(
                    unity=str(commande_data['unite']),
                    quantity=str(commande_data['quantity']),
                    price_indiv=str(commande_data['prixindiv']),
                    price_total=str(commande_data['prixtotal']),
                    sum=str(commande_data['somme']),
                    id_produit=produit
                )

                # Save Client
                client, created = Client.objects.get_or_create(
                    name=str(client_data['namec']),
                    defaults={
                        'address':str( client_data['adressec']),
                        'mail': str(client_data['mail']),
                        'phone': str(client_data['phone']),
                        'fax': str(client_data['fax']),
                        'tax_id': str(client_data['taxid'])
                    }
                )

                # Save BonCommande
                BonCommande.objects.create(
                    date=str(bonCommande_data['date']),
                    id_client=client,
                    fournisseur=fournisseur,
                    id_commande=commande,
                    numero=str(bonCommande_data['number'])
                )

                return JsonResponse({'message': 'Data saved successfully!'})
            except IntegrityError as e: 
                return JsonResponse({'error': 'Database integrity error: ' + str(e)}, status=400)

            except Exception as e:
                return JsonResponse({'error': 'An unexpected error occurred: ' + str(e)}, status=500)

     
        else:
            try:
                upload_file = request.FILES['file']
            except MultiValueDictKeyError:
                return JsonResponse({'error': 'No file was uploaded.'}, status=400)
        
            encodings_to_try = ['utf-8', 'utf-16', 'latin-1', 'cp1256']

            for encoding in encodings_to_try:
             try:
                ftext = upload_file.read().decode(encoding)
                break
             except UnicodeDecodeError:
                continue  

            tables = tablepdf.extract_tables(upload_file)
            table_data = tablepdf.fetch_table_data(tables)
            ftext = pdf.extract_text_per_line(upload_file)

            # Extract Fournisseur data
            identificateur = pdf.extract_remaining_text_from_list(ftext, ":المعرف")
            name = pdf.extract_remaining_text_from_list(ftext, ":االسم واللقب أو االسم االجتماعي")
            address = pdf.extract_remaining_text_from_list(ftext, ":العنوان")
            sujet = pdf.extract_remaining_text_from_list(ftext, "موضوع الطلب:")
            consultation=pdf.extract_remaining_text_from_list(ftext, "consultation").strip()


        
            # Extract Produit data
            produit_name = table_data[4][0]
            produit_characteristic = "\n".join(table_data[4])
       

            # Extract Commande data
            unity = table_data[3]
            quantity = table_data[2]
            price_ind = "\n".join(table_data[1][:-1])
            price_tt = "\n".join(table_data[0][:-1])
            sum_val = table_data[0][-1]



            #Extract client data
            Cname = "كلية العلوم بقابس"
            Caddress = pdf.extract_remaining_text_from_list(ftext, "mail@fsg.rnu.tn").strip()
            Cmail = pdf.extract_remaining_text_from_list(ftext, Caddress).strip()
            Cphone = "75392600"
            Cfax = "75392421"
            Ctax_id = pdf.extract_remaining_text_from_list(ftext,":الهاتف 392600 75 الفاكس 392421 75 المعرف الجبائي")



            # Extract BonCommande data
            date = pdf.extract_remaining_text_from_list(ftext, "المزود").strip()
            numero=pdf.extract_remaining_text_from_list(ftext, "عدد").strip()

            context = {
             #fournisseur
             'identificateur': identificateur,
             'name': name,
             'address': address,
             'sujet': sujet,
             'consultation': consultation,
             #produit
             'pname': produit_name,
             'pchar':produit_characteristic,
             #commande
             'unity':unity,
             'quantity':quantity,
             'prixi':price_ind,
             'prixt':price_tt,
             'somme':sum_val,
             #boncommande
             'date':date,
             'numero':numero,
             #client
             'cname':Cname ,
             'caddress':Caddress ,
             'cmail':Cmail ,
             'cphone':Cphone,
             'cfax':Cfax ,
             'ctax':Ctax_id


            }
            
        return JsonResponse(context) 

    return render(request, 'File.html', {}) 
 
        

    



def home(request):

    return render(request, 'home.html', {} )






def User(request):

    return render(request, 'User.html', {} )


