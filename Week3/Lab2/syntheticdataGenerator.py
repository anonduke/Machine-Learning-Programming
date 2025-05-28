#code adapted from Grok
import pandas as pd
import random
from datetime import datetime, timedelta
import os

# Generate synthetic data
random.seed(42)
cities = ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix", "new york", "LA"]
products = ["Laptop", "Phone", "Tablet", "Headphones", "Charger"]
coupons = ["SAVE10", "SAVE20", "FREESHIP", "INVALID", ""]
start_date = datetime(2024, 1, 1)

data = []
for i in range(500):
    date = start_date + timedelta(days=random.randint(0, 365))
    data.append({
        "date": date.strftime("%m/%d/%Y"),
        "customer_id": f"CUST{random.randint(1000, 9999)}",
        "product": random.choice(products),
        "price": round(random.uniform(10, 1000), 2),
        "quantity": random.randint(1, 10),
        "coupon_code": random.choice(coupons),
        "shipping_city": random.choice(cities)
    })

df = pd.DataFrame(data)
os.makedirs("data", exist_ok=True)
df.to_csv("data/synthetic_sales.csv", index=False)