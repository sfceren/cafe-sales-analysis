"""
Generate realistic cafe sales data for analysis.

Creates a 90-day transaction dataset with realistic patterns:
- Morning coffee rush (8-10 AM)
- Lunch peak (12-14 PM)
- Evening dessert/tea hours
- Higher weekend traffic
- Seasonal product preferences
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta

np.random.seed(42)  # reproducibility

# Product catalog with realistic Turkish cafe pricing (TL)
PRODUCTS = {
    "Espresso":      {"price": 65,  "category": "Coffee",  "morning_boost": 2.5},
    "Latte":         {"price": 95,  "category": "Coffee",  "morning_boost": 2.0},
    "Cappuccino":    {"price": 90,  "category": "Coffee",  "morning_boost": 2.2},
    "Filter Coffee": {"price": 70,  "category": "Coffee",  "morning_boost": 2.8},
    "Black Tea":     {"price": 35,  "category": "Tea",     "morning_boost": 1.3},
    "Green Tea":     {"price": 45,  "category": "Tea",     "morning_boost": 1.0},
    "Cheesecake":    {"price": 140, "category": "Dessert", "morning_boost": 0.4},
    "Brownie":       {"price": 110, "category": "Dessert", "morning_boost": 0.5},
    "Croissant":     {"price": 75,  "category": "Pastry",  "morning_boost": 2.5},
    "Sandwich":      {"price": 130, "category": "Food",    "morning_boost": 0.8},
}

def hour_weight(hour):
    """Customer traffic distribution across the day (8 AM - 10 PM)."""
    # Two peaks: morning rush + evening hangout
    morning_peak = np.exp(-((hour - 9) ** 2) / 4)
    lunch_peak = np.exp(-((hour - 13) ** 2) / 3) * 0.8
    evening_peak = np.exp(-((hour - 19) ** 2) / 5) * 1.1
    return morning_peak + lunch_peak + evening_peak

def generate_transactions(start_date="2024-01-01", days=90):
    records = []
    current = datetime.strptime(start_date, "%Y-%m-%d")

    for day_offset in range(days):
        date = current + timedelta(days=day_offset)
        weekday = date.weekday()  # 0=Mon, 6=Sun
        is_weekend = weekday >= 5

        # Weekend traffic is ~40% higher
        daily_traffic = int(np.random.normal(75, 12) * (1.4 if is_weekend else 1.0))

        for _ in range(max(daily_traffic, 20)):
            # Choose hour based on traffic distribution
            hours = np.arange(8, 23)
            weights = np.array([hour_weight(h) for h in hours])
            weights = weights / weights.sum()
            hour = np.random.choice(hours, p=weights)

            # Product choice depends on time of day
            product_names = list(PRODUCTS.keys())
            base_probs = np.ones(len(product_names))
            for i, name in enumerate(product_names):
                boost = PRODUCTS[name]["morning_boost"]
                if hour < 12:
                    base_probs[i] *= boost
                elif hour >= 17:
                    base_probs[i] *= (2.0 - boost * 0.4)  # evening favors desserts/tea
            base_probs = base_probs / base_probs.sum()

            product = np.random.choice(product_names, p=base_probs)
            quantity = np.random.choice([1, 1, 1, 2, 2, 3], p=[0.45, 0.20, 0.10, 0.15, 0.07, 0.03])

            # Payment method
            payment = np.random.choice(
                ["Card", "Cash", "Mobile"],
                p=[0.62, 0.25, 0.13]
            )

            records.append({
                "transaction_id": f"TX{len(records)+1:05d}",
                "date": date.strftime("%Y-%m-%d"),
                "day_of_week": date.strftime("%A"),
                "hour": int(hour),
                "product": product,
                "category": PRODUCTS[product]["category"],
                "quantity": int(quantity),
                "unit_price": PRODUCTS[product]["price"],
                "total": int(quantity * PRODUCTS[product]["price"]),
                "payment_method": payment,
            })

    df = pd.DataFrame(records)
    return df


if __name__ == "__main__":
    df = generate_transactions()
    df.to_csv("/home/claude/cafe-sales-analysis/data/cafe_sales.csv", index=False)
    print(f"Generated {len(df):,} transactions across {df['date'].nunique()} days")
    print(f"Date range: {df['date'].min()} to {df['date'].max()}")
    print(f"Total revenue: {df['total'].sum():,} TL")
    print(f"\nSample:")
    print(df.head())
