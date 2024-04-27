import tabula  
import fitz  
import camelot  



def extract_tables(pdf_file_path):

    try:
        tables = tabula.read_pdf(pdf_file_path, pages="all", multiple_tables=True)
    except tabula.errors.JavaNotFoundError:
        print("tabula-py requires Java. Trying Camelot as an alternative.")
        try:
            tables = camelot.read_pdf(pdf_file_path, flavor="stream", pages="all", columns=True)
        except Exception as e:
            print("Error using Camelot:", e)
            tables = []

    return tables


def fetch_table_data(tables):
    data = []
    for table in tables:
        transposed_table = table.transpose()  # Transpose the table to switch rows and columns
        for index, column in transposed_table.iterrows():
            # Skip rows with NaN values
            if column.notna().any():
                # Append non-NaN values to data list
                data.append(list(column.dropna()))
    return data



pdf_file_path = "C:/Users/jarra/Downloads/Documents/modele.pdf"

tables = extract_tables(pdf_file_path)
table_data = fetch_table_data(tables)
"""
for column_data in table_data:
   for data in column_data:
       data="\n"+ str(data) 
       print(data)
   print("--------")

"""