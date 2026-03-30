import psycopg2
from psycopg2.extras import execute_values


def load_data(data):
    conn = psycopg2.connect(
        host="postgres",
        database="airflow",
        user="airflow",
        password="airflow"
    )

    cursor = conn.cursor()

    # ✅ FIX: add UNIQUE constraint
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS market_data (
        id SERIAL PRIMARY KEY,
        instrument_id TEXT,
        price FLOAT,
        volume FLOAT,
        timestamp TIMESTAMP,
        vwap FLOAT,
        is_outlier BOOLEAN,
        UNIQUE (instrument_id, timestamp)
    );
    """)

    query = """
    INSERT INTO market_data (
        instrument_id, price, volume, timestamp, vwap, is_outlier
    )
    VALUES %s
    ON CONFLICT (instrument_id, timestamp)
    DO UPDATE SET
        price = EXCLUDED.price,
        volume = EXCLUDED.volume,
        vwap = EXCLUDED.vwap,
        is_outlier = EXCLUDED.is_outlier;
    """

    values = [
        (
            row["instrument_id"],
            row["price"],
            row["volume"],
            row["timestamp"],
            row["vwap"],
            row["is_outlier"]
        )
        for row in data
    ]

    execute_values(cursor, query, values)

    conn.commit()
    cursor.close()
    conn.close()