import re


def clean_text(text):
    text = text.lower()
    text = text.replace(",", "")
    text = text.replace("₹", "")
    text = text.replace("rs.", "")
    return text


def find(patterns, text):
    for p in patterns:
        m = re.search(p, text)
        if m:
            return m.group(1)
    return ""


def parse_invoice(text):

    text = clean_text(text)

    # -----------------------
    # Vendor
    # -----------------------

    vendor = ""

    for line in text.split("\n"):
        if "limited" in line or "pvt" in line:
            vendor = line.strip()
            break

    # -----------------------
    # Invoice number
    # -----------------------

    invoice_number = find([
        r"invoice#([a-z0-9]+)",
        r"invoice no[: ]([a-z0-9]+)",
        r"tax invoice#([a-z0-9]+)"
    ], text)

    # -----------------------
    # Invoice date
    # -----------------------

    invoice_date = find([
        r"dt[: ]([\d]{2}/[\d]{2}/[\d]{4})",
        r"date[: ]([\d]{2}/[\d]{2}/[\d]{4})"
    ], text)

    # -----------------------
    # GST
    # -----------------------

    gst_number = find([
        r"gstn[: #]*([0-9a-z]{15})",
        r"gstin[: ]([0-9a-z]{15})"
    ], text)

    # -----------------------
    # HSN
    # -----------------------

    hsn_code = find([
        r"hsn/sac.*?(\d{6,8})"
    ], text)

    # -----------------------
    # TAX TABLE PARSER
    # -----------------------

    subtotal = 0
    gst_amount = 0
    total_amount = 0

    lines = text.split("\n")

    for line in lines:
        match = re.search(
            r"(\d{6,8})(?:\.0)?\s+(\d+\.\d+)\s+(\d+\.\d+)\s+(\d+\.\d+)",
            line
        )
        if match:
            hsn_code = match.group(1)
            subtotal = float(match.group(2))
            gst_amount = float(match.group(3))
            total_amount = float(match.group(4))
            break

    # -----------------------
    # Return
    # -----------------------

    return {
        "vendor_name": vendor,
        "invoice_number": invoice_number,
        "invoice_date": invoice_date,
        "gst_number": gst_number,
        "hsn_code": hsn_code,
        "subtotal": subtotal,
        "gst_amount": gst_amount,
        "total_amount": total_amount,
        "gst_rate": 0,
        "items": [],
        "surcharges": []
    }