# PDF Form Filler

This Python script reads data from CSV files and fills a PDF form template with the data. It's designed to work with a specific PDF form (Form 8949) and two CSV files (short-term and long-term transactions).

![img.png](img.png)

## Overview

The script consists of several functions that perform the following tasks:

1. **Copy a PDF page with annotations**: Creates a deep copy of a PDF page, including its annotations.
2. **Read CSV data**: Reads data from a CSV file and returns a list of dictionaries.
3. **Process CSV data**: Processes the CSV data and fills the PDF template with the data.
4. **Fill a single PDF page with data**: Fills a single PDF page with data from the CSV.
5. **Fill initial fields**: Fills in the initial fields of the PDF page.
6. **Fill table**: Fills in the 14 x 8 table with data from the CSV.
7. **Fill sum fields**: Fills in the sum fields of the PDF page.

## How It Works

1. The script starts by reading the short-term and long-term transaction data from two CSV files.
2. It then reads the PDF form template (Form 8949) and extracts the short-term and long-term template pages.
3. The script processes the short-term and long-term CSV data separately, filling the corresponding template pages with the data.
4. After processing both sets of data, the script combines the short-term and long-term PDFs into a single output PDF file.

## Usage

1. Ensure you have the required dependencies installed: `pdfrw`.
2. Place your CSV files (short-term and long-term transactions) in the same directory as the script.
3. Update the `short_csv`, `long_csv`, and `template_pdf` variables in the `main()` function to match your file names.
4. Run the script: `python pdf_form_filler.py`.
5. The filled PDF form will be saved in the `output` directory as `output_filled.pdf`.

## Dependencies

- [pdfrw](https://pypi.org/project/pdfrw/): A Python library for reading and writing PDF files.

You can also view these Perplexity threads ([1](https://www.perplexity.ai/search/ff2d8dba-da3f-4f9b-9631-4154253f705b), [2](https://www.perplexity.ai/search/71d8dae8-44b2-407a-81c0-be47efae2dd8?s=u)) with the entire process of debugging and building this code!
