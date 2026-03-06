def check_calculation(invoice):

    subtotal = invoice["subtotal"]
    gst = invoice["gst_amount"]
    total = invoice["total_amount"]

    # Case 1 — GST already included in price (Retail invoices)
    if subtotal == total:
        return None

    # Case 2 — Normal GST calculation
    expected_total = subtotal + gst

    if abs(expected_total - total) > 1:
        return {"error": "Subtotal calculation mismatch"}

    return None