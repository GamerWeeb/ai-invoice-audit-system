import os
from ocr_reader import extract_text_from_pdf
from ai_parser import parse_invoice

def process_invoice_folder(folder):

    invoices = []

    for file in os.listdir(folder):

        if file.endswith(".pdf"):

            path = os.path.join(folder, file)

            text = extract_text_from_pdf(path)

            parsed = parse_invoice(text)

            invoices.append(parsed)

    return invoices