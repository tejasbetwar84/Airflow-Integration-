import os
import requests
import logging
import time

API_URL = os.getenv("API_URL")   \


def extract_data(retries=3, timeout=5):
    if not API_URL:
        raise ValueError("API_URL not set in environment variables")

    for attempt in range(retries):
        try:
            response = requests.get(API_URL, timeout=timeout)

            if response.status_code != 200:
                raise Exception(f"Bad response: {response.status_code}")

            data = response.json()

            if not isinstance(data, list):
                raise Exception("Invalid response format")

            logging.info(f"Extracted {len(data)} records")
            logging.info(f"Sample: {data[:2]}")

            return data

        except Exception as e:
            logging.warning(f"Attempt {attempt+1} failed: {e}")
            time.sleep(2)

    logging.error("Extraction failed after retries")
    return []