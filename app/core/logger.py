import logging
import sys
import json
from datetime import datetime


class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
        }

        if hasattr(record, "extra_data"):
            log_record.update(record.extra_data)

        return json.dumps(log_record)

def get_logger(name: str):
    logger = logging.getLogger(name)

    if not logger.handlers:   # ✅ prevent duplicate handlers
        logger.setLevel(logging.INFO)

        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(JSONFormatter())

        logger.addHandler(handler)
        logger.propagate = False

    return logger