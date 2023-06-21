import os
import csv
from pdfrw import PdfReader, PdfDict, PdfWriter, PdfName


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
    short_csv = "short.csv"
    long_csv = "long.csv"
    template_pdf = "f8949.pdf"
    output_folder = "output"

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    short_data = read_csv_data(short_csv)
    short_pages = (len(short_data) // 14) + 1

    input_template = PdfReader(template_pdf)
    template_page = input_template.pages[0]

    new_pdf = PdfWriter()
    new_pdf_path = "output/output_shell.pdf"
    for i in range(short_pages):
        new_pdf.addPage(template_page)
    new_pdf.write(new_pdf_path)

    new_pdf = PdfReader(new_pdf_path)
    for page in new_pdf.pages:
        annotations = page['/Annots']
        annotations[0].update(PdfDict(V='{}'.format("Mackenzie Patel"), AS='{}'.format("Mackenzie Patel")))
        annotations[1].update(PdfDict(V='{}'.format("420-69-4200"), AS='{}'.format("420-69-4200")))
        annotations[4].update(PdfDict(V=PdfName('On'), AS=PdfName('On')))
        print(annotations[0])
        for annotation in annotations[5:]:
            field_name = annotation['/T'][1:-1]
            field_type = annotation['/FT']

            if field_type == '/Tx':  # Text field
                random_data = "123"
                annotation.update(PdfDict(V='{}'.format(random_data), AS='{}'.format(random_data)))
            else:
                print("Unknown field type:", field_type)

    PdfWriter().write('output/output_filled.pdf', new_pdf)


if __name__ == "__main__":
    main()
