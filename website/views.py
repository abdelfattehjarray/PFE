from django.shortcuts import render
from .models import Client, Fournisseur, BonCommande,Produit, Commande
from .extractcode import pdf
from .extractcode import tablepdf
from django.http import HttpResponse




def home(request):

    return render(request, 'home.html', {} )



def upload(request):
    if request.method == 'POST':

        upload_file = request.FILES['uploadFile']
        encodings_to_try = ['utf-8', 'utf-16', 'latin-1', 'cp1256']  # Add more encodings if needed

        for encoding in encodings_to_try:
            try:
                ftext = upload_file.read().decode(encoding)
                break  # Stop trying encodings if decoding succeeds
            except UnicodeDecodeError:
                continue  



        #put file and data in variables 
        
        
        
        tables = tablepdf.extract_tables(upload_file)
        table_data = tablepdf.fetch_table_data(tables)
        ftext = pdf.extract_text_per_line(upload_file)


        #fournisseur
        identificateur=pdf.extract_remaining_text_from_list( ftext,":المعرف" )
        name=pdf.extract_remaining_text_from_list(ftext, "االسم واللقب أو االسم االجتماعي ")
        address=pdf.extract_remaining_text_from_list(ftext, "العنوان")
        sujet=pdf.extract_remaining_text_from_list(ftext,"موضوع الطلب:")
   
        newf=Fournisseur(identificateur=identificateur, name=name, address=address,sujet=sujet )
        newf.save()


        #produit
        





        return HttpResponse("Code executed successfully.")
   


    return render(request , 'upload.html' , {})
    




    
