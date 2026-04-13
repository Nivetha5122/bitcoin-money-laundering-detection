import random

def generate_behavior():
    illicit = random.random() < 0.2

    if illicit:
        return {
            "amount": random.uniform(2, 6),
            "fee": random.uniform(0.001, 0.005),
            "inputs": random.randint(1, 2),
            "outputs": random.randint(5, 10)
        }
    else:
        return {
            "amount": random.uniform(0.1, 2),
            "fee": random.uniform(0.0001, 0.001),
            "inputs": random.randint(1, 3),
            "outputs": random.randint(1, 3)
        }
