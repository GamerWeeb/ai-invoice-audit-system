def detect_price_anomaly(invoice, historical_prices):

    anomalies = []

    for item in invoice["items"]:

        avg_price = historical_prices.get(item["description"])

        if avg_price:

            if item["rate"] > avg_price * 1.3:

                anomalies.append({
                    "item": item["description"],
                    "rate": item["rate"],
                    "expected": avg_price
                })

    return anomalies