import sys
from django.contrib import messages
from django.db import IntegrityError
from django.urls import reverse
from .models import Client, Fournisseur, BonCommande,Produit, Commande
from .extractcode import pdf, tablepdf
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth.models import User  # Import the User model
from django.utils.datastructures import MultiValueDictKeyError
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import user_passes_test
from django.views.decorators.cache import cache_control
sys.stdout.reconfigure(encoding='utf-8')

def save_data(request):
        if request.method == 'POST':
           
            
                    
            # Get ALL values from request.POST 
            identificateur1 = request.POST.get('identificateur').encode('utf-8').decode('utf-8') 
            name1 = request.POST.get('name').encode('utf-8').decode('utf-8') 
            adresse1 = request.POST.get('adresse').encode('utf-8').decode('utf-8') 
            sujet1 = request.POST.get('sujet').encode('utf-8').decode('utf-8') 
            consultation1 = request.POST.get('consultation').encode('utf-8').decode('utf-8') 

            namep1 = request.POST.get('namep').encode('utf-8').decode('utf-8') 
            characteristic1 = request.POST.get('characteristic').encode('utf-8').decode('utf-8') 

            quantity1 = request.POST.get('quantity').encode('utf-8').decode('utf-8') 
            unite1 = request.POST.get('unite').encode('utf-8').decode('utf-8') 
            prixindiv1 = request.POST.get('prixindiv').encode('utf-8').decode('utf-8') 
            prixtotal1 = request.POST.get('prixtotal').encode('utf-8').decode('utf-8') 
            somme1 = request.POST.get('somme').encode('utf-8').decode('utf-8') 

            namec1 = request.POST.get('namec').encode('utf-8').decode('utf-8') 
            adressec1 = request.POST.get('adressec').encode('utf-8').decode('utf-8') 
            mail1 = request.POST.get('mail').encode('utf-8').decode('utf-8') 
            phone1 = request.POST.get('phone').encode('utf-8').decode('utf-8') 
            fax1 = request.POST.get('fax').encode('utf-8').decode('utf-8') 
            taxid1 = request.POST.get('taxid').encode('utf-8').decode('utf-8') 

            date1 = request.POST.get('date').encode('utf-8').decode('utf-8') 
            number1 = request.POST.get('number').encode('utf-8').decode('utf-8') 
            sys.stdout.flush()

            try: 
                # Save Fournisseur
                fournisseur, created = Fournisseur.objects.get_or_create(
                    identificateur=str(identificateur1),
                    defaults={
                        'name': str(name1),
                        'address': str(adresse1),
                        'sujet': str(sujet1),
                        'consultation': str(consultation1)
                    }
                )

                # Save Produit
                produit, created = Produit.objects.get_or_create(
                    name=str(namep1),
                    characteristic=str(characteristic1)
                )

                # Save Commande
                commande = Commande.objects.create(
                    unity=str(unite1),
                    quantity=str(quantity1),
                    price_indiv=str(prixindiv1),
                    price_total=str(prixtotal1),
                    sum=str(somme1),
                    id_produit=produit
                )

                # Save Client
                client, created = Client.objects.get_or_create(
                    name=str(namec1),
                    defaults={
                        'address': str(adressec1),
                        'mail': str(mail1),
                        'phone': str(phone1),
                        'fax': str(fax1),
                        'tax_id': str(taxid1)
                    }
                )

                # Save BonCommande
                BonCommande.objects.create(
                    date=str(date1),
                    id_client=client,
                    fournisseur=fournisseur,
                    id_commande=commande,
                    numero=str(number1)
                )
                


                return HttpResponseRedirect(reverse('File')) 

            except IntegrityError as e:
                return JsonResponse({'error': 'Database integrity error: ' + str(e)}, status=400)

            except Exception as e:
                return JsonResponse({'error': 'An unexpected error occurred: ' + str(e)}, status=500)
        return redirect("user")


@csrf_exempt
def File(request):
    if request.method == 'POST':
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
            identificateur = pdf.extract_remaining_text_from_list(ftext, ":المعرف").strip()
            name = pdf.extract_remaining_text_from_list(ftext, ":االسم واللقب أو االسم االجتماعي").strip()
            address = pdf.extract_remaining_text_from_list(ftext, ":العنوان").strip()
            sujet = pdf.extract_remaining_text_from_list(ftext, "موضوع الطلب:").strip()
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






def user(request):
    
    return render(request, 'user.html', {} )


   

   





def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('emailL')
        password = request.POST.get('passwordL')

        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            # Redirect to a success page (e.g., home)
            return redirect('home')
        else:
            # Add an error message to the context
            messages.error(request, 'Wrong username or password, try again!')
            return redirect('user')
    else:
        return render(request, 'user.html')
    

    
def logout_view(request):
    logout(request)
    return redirect('user', permanent=True)


def bon_commande(request):
    bon_commande = BonCommande.objects.all()
    return render(request, 'bon_commande.html',{'bon_commande': bon_commande} )


def commandedetails(request):
    if request.method == 'GET':
        try:
            bon_commande_id = request.GET.get('id')
            bon_commande = get_object_or_404(BonCommande, pk=bon_commande_id)

            # Extract data from the BonCommande object for the template
            fournisseur = bon_commande.fournisseur
            client = bon_commande.id_client
            commande = bon_commande.id_commande
            produit = commande.id_produit

            context = {
                'bon_commande': bon_commande,
                'fournisseur': fournisseur,
                'client': client,
                'commande': commande,
                'produit': produit
            }

            return render(request, 'commandedetails.html', context)

        except:
            return render(request, 'commandedetails.html', {'error': 'Invalid BonCommande ID'})
    else:
        return render(request, 'commandedetails.html', {})






def inscription(request):
    if request.method == 'POST':
        username = request.POST.get('firstName')
        email = request.POST.get('email')
        password = request.POST.get('password')
        lastName = request.POST.get('lastName')
        statut = request.POST.get('statut')

        # Check for existing username
        if User.objects.filter(username=username).exists():
            return JsonResponse({'success': False, 'errors': ['Le nom d\'utilisateur est déjà utilisé.']})

        # Create the user with `is_active=False` to set it as inactive
        User.objects.create_user(username=username, email=email, password=password, first_name=username, last_name=lastName, is_active=False)

        # Send success response
        return JsonResponse({'success': True, 'message': 'Utilisateur créé avec succès! Veuillez vérifier votre email pour l\'activation.'})
    
    return render(request, 'user.html', {})