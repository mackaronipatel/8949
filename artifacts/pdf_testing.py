from pdfrw import PdfReader


def list_form_field_names(input_pdf):
    template = PdfReader(input_pdf)
    annotations = template.pages[0]['/Annots']

    field_names = []

    for annotation in annotations:
        field_name = annotation.get('/T')
        if field_name:
            field_names.append(field_name)

    return field_names


input_pdf_path = "f8949.pdf"
field_names = list_form_field_names(input_pdf_path)
print("Field names in the PDF:", len(field_names))
