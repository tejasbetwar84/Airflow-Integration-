from fastapi import FastAPI
import random
from datetime import datetime

app = FastAPI()

instruments = ["AAPL", "GOOG", "BTC-USD", "ETH-USD"]


@app.get("/v1/market-data")
def get_data():
    # 5% failure
    if random.random() < 0.05:
        return {"error": "failure"}

    data = []

    for _ in range(10):
        price = "invalid" if random.random() < 0.05 else round(random.uniform(100, 50000), 2)

        data.append({
            "instrument_id": random.choice(instruments),
            "price": price,
            "volume": round(random.uniform(1, 1000), 2),
            "timestamp": datetime.utcnow().isoformat()
        })

    return data