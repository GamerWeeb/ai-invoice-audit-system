import pandas as pd

def generate_report(issues, invoice):

    if not issues:
        data = [{
            "invoice": invoice.get("invoice_number", ""),
            "vendor": invoice.get("vendor_name", ""),
            "issue": "No discrepancies found",
            "amount": 0
        }]
        return pd.DataFrame(data)

    return pd.DataFrame(issues)