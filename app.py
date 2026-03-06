import streamlit as st
import os
import json
import pandas as pd

from ocr_reader import extract_text_from_pdf
from ai_parser import parse_invoice
from duplicate_detector import detect_duplicate
from gst_validator import validate_gst
from audit_engine import check_calculation
from price_anomaly import detect_price_anomaly
from report_generator import generate_report

st.title("AI Invoice Audit System")

uploaded_files = st.file_uploader(
    "Upload Invoice PDFs",
    type=["pdf"],
    accept_multiple_files=True
)

processed_invoices = []
issues = []

historical_prices = {
    "Freight": 50,
    "Shipping": 60
}

if uploaded_files:

    for file in uploaded_files:

        with open(f"data/{file.name}", "wb") as f:
            f.write(file.getbuffer())

        pdf_path = f"data/{file.name}"

        # OCR Extraction
        text = extract_text_from_pdf(pdf_path)

        # Parse Invoice
        invoice = parse_invoice(text)

        st.subheader(f"Parsed Invoice: {file.name}")
        st.json(invoice)

        # Duplicate Detection
        if detect_duplicate(invoice, processed_invoices):

            issues.append({
                "invoice": invoice["invoice_number"],
                "vendor": invoice["vendor_name"],
                "issue": "Duplicate Invoice",
                "amount": invoice["total_amount"]
            })

        # GST Validation
        gst_issue = validate_gst(invoice)

        if gst_issue:

            issues.append({
                "invoice": invoice["invoice_number"],
                "vendor": invoice["vendor_name"],
                "issue": gst_issue["error"],
                "amount": invoice["gst_amount"]
            })

        # Calculation Check
        calc_issue = check_calculation(invoice)

        if calc_issue:

            issues.append({
                "invoice": invoice["invoice_number"],
                "vendor": invoice["vendor_name"],
                "issue": calc_issue["error"],
                "amount": invoice["total_amount"]
            })

        # Price Anomaly
        anomalies = detect_price_anomaly(invoice, historical_prices)

        for a in anomalies:

            issues.append({
                "invoice": invoice["invoice_number"],
                "vendor": invoice["vendor_name"],
                "issue": "Price Anomaly",
                "amount": a["rate"]
            })

        processed_invoices.append(invoice)

    # Generate report
    report = generate_report(issues, invoice)

    st.subheader("Audit Report")

    # If no issues → show success summary
    if report.empty:

        success_data = [{
            "invoice": invoice["invoice_number"],
            "vendor": invoice["vendor_name"],
            "issue": "No discrepancies found",
            "amount": 0
        }]

        report = pd.DataFrame(success_data)

        st.dataframe(report)

        st.success("Invoice validated successfully. No errors detected.")

        total_overcharge = 0

    else:

        st.dataframe(report)

        total_overcharge = report["amount"].sum()

        st.subheader("Issues by Vendor")

        vendor_summary = report.groupby("vendor")["amount"].sum()

        st.bar_chart(vendor_summary)

        st.subheader("Issues by Type")

        issue_summary = report.groupby("issue")["amount"].sum()

        st.bar_chart(issue_summary)

    # KPI
    st.metric("Total Overcharges Detected", f"₹{total_overcharge}")