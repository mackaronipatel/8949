import os
import csv
from pdfrw import PdfReader, PdfDict, PdfWriter


def read_csv_data(file_path):
    with open(file_path, newline='', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        data = [row for row in reader]
    return data


def fill_with_empty_data():
    input_pdf_path = "f8949.pdf"
    template = PdfReader(input_pdf_path)
    annotations = template.pages[0]['/Annots']

    for annotation in annotations:
        field_name = annotation['/T'][1:-1]  # Extract the field name
        field_type = annotation['/FT']

        if field_type == '/Tx':  # Text field
            random_data = "123"
            annotation.update(PdfDict(V='{}'.format(random_data), AS='{}'.format(random_data)))
        else:
            print("Unknown field type:", field_type)

    PdfWriter().write('output_test.pdf', template)


def main():
    csv_file_path = "import_csv.csv"
    input_pdf_path = "f8949.pdf"
    output_folder = "output_forms"

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    data = read_csv_data(csv_file_path)
    print(data)

    fill_with_empty_data()


if __name__ == "__main__":
    main()
