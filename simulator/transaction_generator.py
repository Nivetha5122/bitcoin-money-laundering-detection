import random
import string
from datetime import datetime, timezone

def rand_addr():
    return "bc1" + "".join(
        random.choices(string.ascii_lowercase + "0123456789", k=30)
    )

def generate_transaction():
    return {
        "timestamp": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "sender": rand_addr(),
        "receivers": [rand_addr() for _ in range(random.randint(1, 5))],
        "amount": round(random.uniform(0.1, 5.0), 4),
        "fee": round(random.uniform(0.0001, 0.001), 6),
        "inputs": random.randint(1, 4)
    }
