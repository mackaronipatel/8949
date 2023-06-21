import csv
from PyPDFForm import PyPDFForm

def fill_form_8949(input_csv, input_pdf, output_pdf):
    with open(input_csv, "r") as csvfile:
        csv_reader = csv.reader(csvfile)
        next(csv_reader)  # Skip header row

        data = []
        for row in csv_reader:
            data.append({
                "Description": row[0],
                "Date Acquired": row[1],
                "Date Sold": row[2],
                "Proceeds": row[3],
                "Cost Basis": row[4],
                "Gain or Loss": row[5]
            })

    form = PyPDFForm(input_pdf)

    for i, row in enumerate(data):
        index = i % 14
        page_number = i // 14

        if index == 0 and page_number > 0:
            form.add_page()

        form.fill({
            f"Description_{index + 1}": row["Description"],
            f"Date Acquired_{index + 1}": row["Date Acquired"],
            f"Date Sold_{index + 1}": row["Date Sold"],
            f"Proceeds_{index + 1}": row["Proceeds"],
            f"Cost Basis_{index + 1}": row["Cost Basis"],
            f"Gain or Loss_{index + 1}": row["Gain or Loss"]
        }, page_number)

    form.save(output_pdf)

input_csv = "your_input_csv_file.csv"
input_pdf = "Form_8949_template.pdf"
output_pdf = "Form_8949_filled.pdf"

fill_form_8949(input_csv, input_pdf, output_pdf)