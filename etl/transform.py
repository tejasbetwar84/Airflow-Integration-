import logging

def transform_data(data):
    transformed = []

    for row in data:
        try:
            price = float(row["price"])
            volume = float(row["volume"])

            vwap = price  # simple logic (can improve later)

            transformed.append({
                "instrument_id": row["instrument_id"],
                "price": price,
                "volume": volume,
                "timestamp": row["timestamp"],
                "vwap": vwap,
                "is_outlier": price > 50000  # example rule
            })

        except Exception as e:
            logging.warning(f"Transform failed for row {row}: {e}")

    return transformed