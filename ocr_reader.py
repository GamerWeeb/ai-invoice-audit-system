from pdf2image import convert_from_path
import pytesseract
import pandas as pd


def extract_text_from_pdf(pdf_path):

    images = convert_from_path(pdf_path)

    full_text = ""

    for img in images:

        data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DATAFRAME)

        data = data[data.conf > 30]

        lines = data.groupby(["block_num", "line_num"])["text"].apply(lambda x: " ".join(x))

        for line in lines:
            full_text += line + "\n"

    return full_text