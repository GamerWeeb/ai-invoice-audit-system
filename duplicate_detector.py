def detect_duplicate(invoice, processed):

    for inv in processed:

        if (
            inv["invoice_number"] == invoice["invoice_number"]
            and inv["vendor_name"] == invoice["vendor_name"]
        ):
            return True

    return False