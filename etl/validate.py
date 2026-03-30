import logging
from typing import List
from datetime import datetime
from pydantic import BaseModel, ValidationError


class MarketData(BaseModel):
    instrument_id: str
    price: float
    volume: float
    timestamp: datetime


def validate_data(data: List[dict]):
    valid_data = []
    dropped = 0

    for record in data:
        try:
            validated = MarketData(**record)
            valid_data.append(validated.dict())
        except ValidationError as e:
            logging.warning(f"Validation failed: {e}")
            dropped += 1

    logging.info(f"Valid records: {len(valid_data)}, Dropped: {dropped}")
    return valid_data