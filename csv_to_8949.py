import os
import csv
from pdfrw import PdfReader, PdfDict, PdfWriter, PdfName


def compare_memory(pdf):
    """Compare the memory addresses of annotations on each page of a PDF. Used for debugging."""
    all_annotations = []
    for page in pdf.pages:
        annotations = page['/Annots']
        all_annotations.append(annotations)

    for i in range(len(all_annotations[0])):
        print(f"Annotation {i}:")
        for page_num, annotations in enumerate(all_annotations):
            annotation = annotations[i]
            print(f"  Page {page_num + 1}: Memory address: {id(annotation)}")
        print()


def copy_page_with_annotations(page):
    """Create a deep copy of a PDF page, including its annotations."""
    new_page = PdfDict(page)
    if PdfName.Annots in new_page:
        new_page[PdfName.Annots] = [PdfDict(annotation) for annotation in new_page[PdfName.Annots]]
    return new_page


def read_csv_data(file_path):
    """Read CSV data from the given file path and return a list of dictionaries."""
    with open(file_path, newline='', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        data = [row for row in reader]
    return data


def process_csv_data(csv_data, template_page, keys, key):
    """Process CSV data and fill the PDF template with the data."""
    num_pages = (len(csv_data) // 14) + 1
    pdf = PdfWriter()
    pdf_path = f"output/output_shell{key}.pdf"

    # Create a new PDF with the required number of pages
    for _ in range(num_pages):
        new_page = copy_page_with_annotations(template_page)
        pdf.addPage(new_page)

    pdf.write(pdf_path)
    pdf = PdfReader(pdf_path)

    # Fill the PDF with data from the CSV
    index_offset = 0
    for page in pdf.pages:
        fill_pdf_page_with_data(page, csv_data, keys, index_offset)
        index_offset += 14 * 8

    return pdf


def fill_pdf_page_with_data(page, csv_data, keys, index_offset):
    """Fill a single PDF page with data from the CSV."""
    annotations = page['/Annots']

    # Fill in the initial fields
    fill_initial_fields(annotations)

    # Fill in the 14 x 8 table
    proceeds_sum, costbasis_sum, gain_loss_sum = fill_table(annotations, csv_data, keys, index_offset)

    # Fill in the sum fields
    fill_sum_fields(annotations, proceeds_sum, costbasis_sum, gain_loss_sum)


def fill_initial_fields(annotations):
    """Fill in the initial fields of the PDF page."""
    annotations[0].update(PdfDict(V='{}'.format("Mackenzie Patel"), AS='{}'.format("Mackenzie Patel")))
    annotations[1].update(PdfDict(V='{}'.format("420-69-4200"), AS='{}'.format("420-69-4200")))
    annotations[4].update(PdfDict(V=PdfName('On'), AS=PdfName('On')))


def fill_table(annotations, csv_data, keys, index_offset):
    """Fill in the 14 x 8 table with data from the CSV."""
    proceeds_sum, costbasis_sum, gain_loss_sum = 0, 0, 0
    for i, annotation in enumerate(annotations[5:-5]):
        i += index_offset
        field_type = annotation['/FT']

        if field_type == '/Tx':
            row = (i // 8)
            col = i % 8

            if row < len(csv_data):
                value = csv_data[row].get(keys[col])
            else:
                break

            annotation.update(PdfDict(V='{}'.format(value), AS='{}'.format(value)))

            # Columns we need to sum
            if col == 3:
                proceeds_value = float(value.replace('$', '').replace(',', ''))
                proceeds_sum += proceeds_value
            elif col == 4:
                costbasis_value = float(value.replace('$', '').replace(',', ''))
                costbasis_sum += costbasis_value
            elif col == 7:
                gain_loss_value = float(value.replace('$', '').replace(',', ''))
                gain_loss_sum += gain_loss_value
        else:
            print("Unknown field type:", field_type)

    return proceeds_sum, costbasis_sum, gain_loss_sum


def fill_sum_fields(annotations, proceeds_sum, costbasis_sum, gain_loss_sum):
    """Fill in the sum fields of the PDF page."""
    annotations[-5].update(PdfDict(V='{}'.format(f"${proceeds_sum}"), AS='{}'.format(proceeds_sum)))
    annotations[-4].update(PdfDict(V='{}'.format(f"${costbasis_sum}"), AS='{}'.format(costbasis_sum)))
    annotations[-1].update(PdfDict(V='{}'.format(f"${gain_loss_sum}"), AS='{}'.format(gain_loss_sum)))


def main():
    short_csv = "short.csv"
    long_csv = "long.csv"
    template_pdf = "f8949.pdf"
    output_folder = "output"

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    keys = ['Asset', 'Date Acquired', 'Date Sold', 'Proceeds', 'Cost Basis', 'Empty1', ' Empty2', 'Gain or Loss']
    input_template = PdfReader(template_pdf)
    short_template_page = input_template.pages[0]
    long_template_page = input_template.pages[1]

    short_data = read_csv_data(short_csv)
    long_data = read_csv_data(long_csv)

    short_pdf = process_csv_data(short_data, short_template_page, keys, "short")
    long_pdf = process_csv_data(long_data, long_template_page, keys, "long")

    # Combine short_pdf and long_pdf
    combined_pdf = PdfWriter()
    for page in short_pdf.pages:
        combined_pdf.addPage(page)
    for page in long_pdf.pages:
        combined_pdf.addPage(page)

    combined_pdf.write('output/output_filled.pdf')


if __name__ == "__main__":
    main()
