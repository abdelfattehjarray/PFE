import sys
from django.contrib import messages
from django.db import IntegrityError
from django.urls import reverse
from django.core.mail import send_mail 
from pfe.settings import EMAIL_HOST_USER
from .models import Client, Fournisseur, BonCommande,Produit, Commande,userstatus
from .extractcode import pdf, tablepdf
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import cache_control
from django.contrib.auth.models import User  
from django.utils.datastructures import MultiValueDictKeyError
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import UserForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm




sys.stdout.reconfigure(encoding='utf-8')



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def home(request):

    return render(request, 'home.html', {} )


def user(request):
    
    return render(request, 'user.html', {} )



#file

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
                


                return redirect('File') 

            except IntegrityError as e:
                return JsonResponse({'error': 'Database integrity error: ' + str(e)}, status=400)

            except Exception as e:
                return JsonResponse({'error': 'An unexpected error occurred: ' + str(e)}, status=500)
        return redirect("user")

@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
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
            produit_characteristic=""
            for item in table_data[4]:
               produit_characteristic +=  item+ "\n"
       

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
 
        

    
















#login and sign up
def loginerror(request):
        return render(request, 'user.html', {})

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('emailL')
        password = request.POST.get('passwordL')

        user = authenticate(request, username=email, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                # Redirect to a success page (e.g., home)
                return redirect('home')
            
            
        else:
            # Add an error message to the context
            messages.error(request, 'Wrong username or password, or account is not active !')
            return redirect('user')
    else:
        return render(request, 'user.html')
    

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
        else:
            # Create the user
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=username,
                last_name=lastName,
                is_active=False
            )

            # Create userstatus after creating the User object
            userstatus.objects.create(status=statut, id_user=user)

            # Send success response as JSON
            return JsonResponse({'success': True})
    return render(request, 'user.html', {})
    




















#boncommandes , commandes
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def bon_commande(request):
    boncommande = BonCommande.objects.all()
    return render(request, 'bon_commande.html',{'boncommande': boncommande} )

@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def commandedetails(request):
    if request.method == 'GET':
        try:
            
            boncommande_id = request.GET.get('id')
            boncommande_id1 = request.GET.get('boncommande_id')

            
            if boncommande_id:

              boncommande = get_object_or_404(BonCommande, pk=boncommande_id)
              # Extract data from the BonCommande object for the template
              fournisseur = boncommande.fournisseur
              client = boncommande.id_client
              commande = boncommande.id_commande
              produit = commande.id_produit

            if boncommande_id1:
               boncommande = get_object_or_404(BonCommande, id=boncommande_id1)
               fournisseur = boncommande.fournisseur
               client = boncommande.id_client
               commande = boncommande.id_commande
               produit = commande.id_produit

            context = {
                'boncommande': boncommande,
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



def deletecommande(request):
    id=request.POST.get('id')
    BC=BonCommande.objects.get(id=id)
    c=Commande.objects.get(id=BC.id_commande.id)
    c.delete()
    
    BC.delete()
    return redirect('bon_commande')

















    #founisseurs 
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def gestionf(request):
    f_ournisseur = Fournisseur.objects.all()
  
    return render(request, 'gestionfournisseur.html',{'f_ournisseur': f_ournisseur} )


def deletef(request):
    id=request.POST.get('id')
    fr=Fournisseur.objects.get(id=id)
    fr.delete()
    return redirect('gestionf')



  #boncommande de fournisseur
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def Fcommande(request):
    if request.method == 'GET':
        f_id = request.GET.get('id')
        if f_id:
            try:
                f = get_object_or_404(Fournisseur, pk=f_id)
                bon_commandes = BonCommande.objects.filter(fournisseur=f)
                context = {'f': f, 'bon_commandes': bon_commandes}
                return render(request, 'Fcommande.html', context)
            except:
                return render(request, 'Fcommande.html', {'error': 'Invalid ID'})
        else:
            # Handle case where no 'id' is provided 
            f_ournisseur = Fournisseur.objects.all()
            return render(request, 'Fcommande.html', {'f_ournisseur': f_ournisseur})
    else:
        return render(request, 'Fcommande.html', {})


@login_required
def deletecf(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        supplier_id = request.POST.get('supplier_id')
        B_C = BonCommande.objects.get(id=id)
        
        B_C.delete()
        return redirect(reverse('Fcommande') + f'?id={supplier_id}') 
    return redirect('Fcommande')











def is_superuser(user):
    return user.is_superuser

def is_staff(user):
    return user.is_staff





#userinterface 
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
@user_passes_test(is_superuser)
def userinterface(request):
    activeusers = User.objects.filter(is_active=True)
    inactive_users=User.objects.filter(is_active=False)

    for inactive_user in inactive_users:
        # Get the userstatus associated with this user
        try:
            user_status = userstatus.objects.get(id_user=inactive_user)
            inactive_user.user_status = user_status.status
        except userstatus.DoesNotExist:
            # If no userstatus exists, set it to "None"
            inactive_user.user_status = "None"


    return render(request, 'userinterface.html', {'activeusers': activeusers, 'inactive_users':inactive_users})


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def activate_user(request):
    if request.method == 'POST':
        user_id = request.POST.get('id')
        permission = request.POST.get('permission')
        

        try:
            user = User.objects.get(pk=user_id)
            if permission in ['staff', 'superuser', 'viewer']:
             user.is_active = True

             if permission == 'staff':
                user.is_staff = True
                user.is_superuser = False
             elif permission == 'superuser':
                user.is_staff = True  # Superusers are always staff
                user.is_superuser = True
             
                

             user.save()


             subject = 'Your account is now active!'
             message = f"Hello {user.username},\n\nYour account is now active. You can now log in to the system.\n\nBest regards,\nThe FSG Team"
             from_email = EMAIL_HOST_USER
             recipient_list = [user.email]
             send_mail(subject, message, from_email, recipient_list)
             return redirect('userinterface')  # Redirect to the userinterface view
            else:
                messages.error(request, 'Please select a valid role.')
                return redirect('userinterface')
        except User.DoesNotExist:
            return render(request, 'userinterface.html', {'error_message': 'User not found'})
        
    else:
        return render(request, 'userinterface.html', {'error_message': 'Invalid request'})
def inactivate_user(request):
    if request.method == 'POST':
        user_id = request.POST.get('id')

        try:
            user = User.objects.get(pk=user_id)
            user.is_active = False

            

            user.save()


            subject = 'Your account is Disabled!'
            message = f"Hello {user.username},\n\nYour account is Disabled. Check with administration for more details.\n\nBest regards,\nThe FSG Team"
            from_email = EMAIL_HOST_USER
            recipient_list = [user.email]
            send_mail(subject, message, from_email, recipient_list)
            return redirect('userinterface')  # Redirect to the userinterface view
        except User.DoesNotExist:
            return render(request, 'userinterface.html', {'error_message': 'User not found'})
    else:
        return render(request, 'userinterface.html', {'error_message': 'Invalid request'})

def deleteuser(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        user = User.objects.get(pk=id)
        user.delete()
        return redirect('userinterface') 
    return redirect('userinterface')










def logout_view(request):
    logout(request)
    return redirect('user', permanent=True)









@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
@user_passes_test(is_superuser)
@user_passes_test(is_staff)
def edit_item(request, item_type, item_id):
    if item_type == 'client':
        item = get_object_or_404(Client, id=item_id)
    elif item_type == 'commande':
        item = get_object_or_404(Commande, id=item_id)
    elif item_type == 'produit':
        item = get_object_or_404(Produit, id=item_id)
    elif item_type == 'fournisseur':
        item = get_object_or_404(Fournisseur, id=item_id)
    else:
        return redirect('home')

    if request.method == 'POST':
        # Process the form data and update the item
        if item_type == 'client':
            item.name = request.POST.get('name')
            item.address = request.POST.get('address')
            item.mail = request.POST.get('mail')
            item.phone = request.POST.get('phone')
            item.fax = request.POST.get('fax')
            item.tax_id = request.POST.get('tax_id')
            
        elif item_type == 'commande':
            item.quantity = request.POST.get('quantity')
            item.unity = request.POST.get('unity')
            item.price_indiv = request.POST.get('price_indiv')
            item.price_total = request.POST.get('price_total')
            item.sum = request.POST.get('sum')
            
        elif item_type == 'produit':
            item.name = request.POST.get('name')
            item.characteristic = request.POST.get('characteristic')
            
        elif item_type == 'fournisseur':
            item.name = request.POST.get('name')
            item.address = request.POST.get('address')
            item.sujet = request.POST.get('sujet')
            item.consultation = request.POST.get('consultation')
            item.save()
            return redirect(reverse('gestionf'))
        else:
            return redirect('home')
        item.save()
        boncommande_id = request.GET.get('boncommande_id')  
        return redirect(reverse('commandedetails') + f'?boncommande_id={boncommande_id}')


         

    context = {
        'item': item,
        'item_type': item_type,
        'boncommande_id': request.GET.get('boncommande_id'),
    }
    return render(request, 'edit_item.html', context)











@login_required
def profile_settings(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        password_form = PasswordChangeForm(request.user, request.POST)

        if 'update_profile' in request.POST:
            if user_form.is_valid():
                user_form.save()
                messages.success(request, 'Your profile was successfully updated!')
                return redirect('profile_settings')
            else:
                messages.error(request, 'Please correct the error below.')

        elif 'change_password' in request.POST:
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)  # Important!
                messages.success(request, 'Your password was successfully updated!')
                return redirect('profile_settings')
            else:
                messages.error(request, 'Please correct the error below.')

    else:
        user_form = UserForm(instance=request.user)
        password_form = PasswordChangeForm(request.user)

    return render(request, 'profile_settings.html', {
        'user_form': user_form,
        'password_form': password_form
    })