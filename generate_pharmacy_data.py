import os
import random
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

# Directory setup
SCRATCH_DIR = "/workspace/scratch/pharmacy_dataset"
OUT_DIR = "/workspace/out"
os.makedirs(SCRATCH_DIR, exist_ok=True)
os.makedirs(OUT_DIR, exist_ok=True)

# ---------------------------------------------------------
# 1. GENERATE PRODUCTS DATASET
# ---------------------------------------------------------
categories_products = {
    "Antibiotics": ["Amoxicillin 500mg", "Azithromycin 250mg", "Ciprofloxacin 500mg", "Cephalexin 500mg", "Doxycycline 100mg", "Augmentin 625mg"],
    "Pain Relief & Anti-inflammatory": ["Paracetamol 500mg", "Ibuprofen 400mg", "Diclofenac 50mg", "Tramadol 50mg", "Naproxen 250mg", "Aspirin 81mg"],
    "Cardiovascular": ["Atorvastatin 20mg", "Amlodipine 5mg", "Lisnopril 10mg", "Losartan 50mg", "Metoprolol 50mg", "Clopidogrel 75mg"],
    "Antidiabetics": ["Metformin 500mg", "Gliclazide 80mg", "Sitagliptin 100mg", "Empagliflozin 10mg", "Insulin Glargine 100IU/ml"],
    "Respiratory": ["Salbutamol Inhaler 100mcg", "Montelukast 10mg", "Fluticasone Inhaler", "Cetirizine 10mg", "Loratadine 10mg"],
    "Gastrointestinal": ["Omeprazole 20mg", "Pantoprazole 40mg", "Ranitidine 150mg", "Loperamide 2mg", "Domperidone 10mg"],
    "Vitamins & Supplements": ["Vitamin D3 1000IU", "Vitamin C 500mg", "Calcium + D3", "B-Complex Ultra", "Zinc 50mg", "Omega-3 Fish Oil 1000mg"],
    "Dermatology & Topical": ["Hydrocortisone Cream 1%", "Clotrimazole Cream 1%", "Betamethasone Ointment", "Mupirocin Ointment 2%"]
}

product_list = []
prod_counter = 1

for cat, items in categories_products.items():
    for item in items:
        prod_id = f"PRD{prod_counter:03d}"
        unit_cost = round(random.uniform(1.50, 45.00), 2)
        margin_multiplier = random.uniform(1.30, 2.10)
        selling_price = round(unit_cost * margin_multiplier, 2)
        lead_time = random.choice([3, 5, 7, 10, 14, 21])
        reorder_level = random.choice([30, 50, 100, 150, 200, 300])
        
        product_list.append({
            "product_id": prod_id,
            "product_name": item,
            "category": cat,
            "unit_cost_usd": unit_cost,
            "selling_price_usd": selling_price,
            "supplier_lead_time_days": lead_time,
            "reorder_level_units": reorder_level
        })
        prod_counter += 1

df_products = pd.DataFrame(product_list)
df_products.to_csv(f"{SCRATCH_DIR}/pharmacy_products.csv", index=False)

# ---------------------------------------------------------
# 2. GENERATE INVENTORY BATCHES DATASET
# ---------------------------------------------------------
batch_list = []
batch_counter = 101
reference_date = datetime(2026, 10, 26) # Current date context

for _, prod in df_products.iterrows():
    # Each product gets 3 to 6 batches received over the past 18 months
    num_batches = random.randint(3, 6)
    
    for _ in range(num_batches):
        batch_id = f"BAT-2025-{batch_counter}"
        batch_counter += 1
        
        # Received date between Oct 2024 and Oct 2026
        days_ago_received = random.randint(30, 600)
        received_dt = reference_date - timedelta(days=days_ago_received)
        
        # Shelf life between 6 months and 24 months from receipt
        shelf_life_days = random.choice([180, 270, 365, 540, 720])
        expiry_dt = received_dt + timedelta(days=shelf_life_days)
        
        qty_received = random.choice([100, 200, 300, 500, 750, 1000])
        
        # If expired long ago, stock should be low or written off; if near-expiry/future, stock varies
        days_to_expiry = (expiry_dt - reference_date).days
        
        if days_to_expiry < -60:
            # Expired in the past
            current_stock = random.choice([0, 0, 0, 15, 30, 45]) # Some remaining = write-off waste
        elif -60 <= days_to_expiry <= 90:
            # Expired recently or near-expiry (0 to 90 days out)
            current_stock = random.randint(20, 250)
        else:
            # Normal fresh stock
            current_stock = random.randint(50, qty_received)
            
        storage_type = "Cold Storage" if prod["category"] in ["Antidiabetics", "Antibiotics"] and random.random() < 0.3 else "Room Temp"
        
        batch_list.append({
            "batch_id": batch_id,
            "product_id": prod["product_id"],
            "received_date": received_dt.strftime("%Y-%m-%d"),
            "expiry_date": expiry_dt.strftime("%Y-%m-%d"),
            "quantity_received": qty_received,
            "current_stock_quantity": current_stock,
            "storage_type": storage_type
        })

df_batches = pd.DataFrame(batch_list)
df_batches.to_csv(f"{SCRATCH_DIR}/pharmacy_inventory_batches.csv", index=False)

# ---------------------------------------------------------
# 3. GENERATE DAILY SALES TRANSACTIONS DATASET
# ---------------------------------------------------------
sales_list = []
start_date = datetime(2025, 10, 1)
end_date = datetime(2026, 10, 25)
total_days = (end_date - start_date).days + 1

txn_counter = 10001

for day_idx in range(total_days):
    current_day = start_date + timedelta(days=day_idx)
    date_str = current_day.strftime("%Y-%m-%d")
    
    # Day of week seasonality: weekends higher sales
    day_weight = 1.3 if current_day.weekday() in [5, 6] else 1.0
    
    # Winter season (Nov-Feb) boost for cough/cold/antibiotics
    month = current_day.month
    winter_boost = 1.25 if month in [11, 12, 1, 2] else 1.0
    
    # Daily transactions count
    daily_txns_count = int(random.randint(15, 35) * day_weight)
    
    for _ in range(daily_txns_count):
        # Pick random active batch that was received before or on current_day
        valid_batches = df_batches[
            (df_batches["received_date"] <= date_str) & 
            (df_batches["expiry_date"] >= (current_day - timedelta(days=30)).strftime("%Y-%m-%d"))
        ]
        
        if valid_batches.empty:
            continue
            
        selected_batch = valid_batches.sample(1).iloc[0]
        prod_info = df_products[df_products["product_id"] == selected_batch["product_id"]].iloc[0]
        
        # Determine sales volume
        base_qty = random.randint(1, 8)
        if prod_info["category"] in ["Antibiotics", "Respiratory"] and winter_boost > 1.0:
            units_sold = int(base_qty * winter_boost)
        else:
            units_sold = base_qty
            
        days_until_exp = (datetime.strptime(selected_batch["expiry_date"], "%Y-%m-%d") - current_day).days
        
        # Clearance discount if batch is within 30 days of expiry
        discount_applied = 1 if (0 < days_until_exp <= 30) else 0
        discount_pct = 0.25 if discount_applied else 0.0
        
        unit_price = round(prod_info["selling_price_usd"] * (1 - discount_pct), 2)
        total_revenue = round(units_sold * unit_price, 2)
        
        sales_list.append({
            "transaction_id": f"TXN-{txn_counter}",
            "transaction_date": date_str,
            "product_id": prod_info["product_id"],
            "batch_id": selected_batch["batch_id"],
            "units_sold": units_sold,
            "unit_price_usd": unit_price,
            "total_revenue_usd": total_revenue,
            "clearance_discount_applied": discount_applied
        })
        txn_counter += 1

df_sales = pd.DataFrame(sales_list)
df_sales.to_csv(f"{SCRATCH_DIR}/pharmacy_sales_transactions.csv", index=False)

print(f"Products dataset: {df_products.shape[0]} rows")
print(f"Batches dataset: {df_batches.shape[0]} rows")
print(f"Sales transactions dataset: {df_sales.shape[0]} rows")
