from django.shortcuts import render
from .models import Client, Fournisseur, BonCommande,Produit, Commande
from .extractcode import pdf
from .extractcode import tablepdf
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404



def home1(request):

    return render(request, 'home1.html', {} )


def home(request):

    return render(request, 'home.html', {} )



def User(request):

    return render(request, 'User.html', {} )


from django.shortcuts import render, get_object_or_404
from .models import Fournisseur, Produit, Commande, BonCommande
from .extractcode import pdf, tablepdf
from django.http import HttpResponse

def upload(request):
    if request.method == 'POST':
        upload_file = request.FILES['uploadFile']
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


        # Check if Fournisseur already exists
        fournisseur, created = Fournisseur.objects.get_or_create(
            identificateur=identificateur,
            defaults={'name': name, 'address': address, 'sujet': sujet, 'consultation':consultation}
        )

        # Extract Produit data
        produit_name = table_data[4][0]
        produit_characteristic = "\n".join(table_data[4])

        # Check if Produit already exists
        produit, created = Produit.objects.get_or_create(
            name=produit_name,
            characteristic=produit_characteristic
        )

        # Extract Commande data
        unity = table_data[3]
        quantity = table_data[2]
        price_ind = "\n".join(table_data[1][:-1])
        price_tt = "\n".join(table_data[0][:-1])
        sum_val = table_data[0][-1]

        # Create Commande
        commande = Commande.objects.create(
            unity=unity,
            quantity=quantity,
            price_indiv=price_ind,
            price_total=price_tt,
            sum=sum_val,
            id_produit=produit
        )

        #Extract client data
        Cname = "كلية العلوم بقابس"
        Caddress = pdf.extract_remaining_text_from_list(ftext, "mail@fsg.rnu.tn").strip()
        Cmail = pdf.extract_remaining_text_from_list(ftext, Caddress).strip()
        Cphone = "75392600"
        Cfax = "75392421"
        Ctax_id = pdf.extract_remaining_text_from_list(ftext,":الهاتف 392600 75 الفاكس 392421 75 المعرف الجبائي")

        #Check if Client already exists
        client, created = Client.objects.get_or_create(
            name=Cname,
            address=Caddress,
            mail=Cmail,
            phone=Cphone,
            fax=Cfax,
            tax_id=Ctax_id
            
        )



        # Extract BonCommande data
        date = pdf.extract_remaining_text_from_list(ftext, "المزود").strip()
        numero=pdf.extract_remaining_text_from_list(ftext, "عدد").strip()
        # Create BonCommande
        BonCommande.objects.create(
            date=date,
            id_client=client,
            fournisseur=fournisseur,
            id_commande=commande,
            numero=numero
        )

        


        return HttpResponse("Code executed successfully.")

    return render(request, 'upload.html', {})
