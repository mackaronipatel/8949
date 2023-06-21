import csv
import os
import pdfrw

def read_csv_data(file_path):
    with open(file_path, newline='', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        data = [row for row in reader]
    print(data)
    return data

def fill_form_8949(input_pdf, output_pdf, data):
    template = pdfrw.PdfReader(input_pdf)
    annotations = template.pages[0]['/Annots']

    for index, row in enumerate(data, start=1):
        prefix = f"{index}_"
        field_data = {
            f"{prefix}a": row["Asset"],
            f"{prefix}b": row["Date Acquired"],
            f"{prefix}c": row["Date Sold"],
            f"{prefix}d": row["Proceeds"],
            f"{prefix}e": row["Cost Basis"],
            f"{prefix}g": row["Gain or Loss"],
        }

        for annotation in annotations:
            field_name = annotation.get('/T')
            if field_name:
                #field_name = field_name.decode('utf-8')
                if field_name in field_data:
                    annotation.update(pdfrw.PdfDict(V='{}'.format(field_data[field_name])))

        if index == 14:
            break

    pdfrw.PdfWriter().write(output_pdf, template)

def main():
    csv_file_path = "import_csv.csv"  # Replace with your CSV file path
    input_pdf_path = "f8949.pdf"  # Replace with your Form 8949 template file path
    output_folder = "output_forms"

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    data = read_csv_data(csv_file_path)
    num_forms = -(-len(data) // 14)  # Calculate the number of forms needed

    for i in range(num_forms):
        start = i * 14
        end = start + 14
        form_data = data[start:end]
        output_pdf_path = os.path.join(output_folder, f"form_8949_{i + 1}.pdf")
        fill_form_8949(input_pdf_path, output_pdf_path, form_data)

if __name__ == "__main__":
    main()