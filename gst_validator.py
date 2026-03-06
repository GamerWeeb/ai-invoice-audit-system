HSN_GST_MAP = {
    "9963": 5,
    "996331": 5,
    "9968": 18,
    "9983": 18,
    "9403": 12
}


def validate_gst(invoice):

    hsn = str(invoice.get("hsn_code", ""))
    subtotal = invoice.get("subtotal", 0)
    gst_amount = invoice.get("gst_amount", 0)

    if subtotal == 0:
        return None

    actual_rate = (gst_amount / subtotal) * 100

    expected_rate = HSN_GST_MAP.get(hsn)

    if expected_rate and abs(actual_rate - expected_rate) > 1:
        return {
            "error": "GST rate mismatch",
            "expected": expected_rate,
            "found": round(actual_rate, 2)
        }

    return None