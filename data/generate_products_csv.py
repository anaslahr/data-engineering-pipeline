import csv
import random
from datetime import datetime, timedelta

# Generate random metadata
def random_date(start, end):
    """Generate a random date between start and end."""
    delta = end - start
    random_days = random.randint(0, delta.days)
    return start + timedelta(days=random_days)

categories = ['Electronics', 'Home Appliances', 'Sports', 'Wearables', 'Books']
suppliers = ['Dell', 'Logitech', 'Apple', 'Philips', 'Sony', 'Nike', 'Ninja', 'Adidas', 'Amazon', 'Fitbit']

# File path
output_file = "products_enriched.csv"

# Generate data
with open(output_file, mode="w", newline="") as file:
    writer = csv.writer(file)
    # Write header
    writer.writerow([
        "product_id", "name", "category", "price", "stock_quantity", "supplier", "description",
        "weight", "dimensions", "warranty", "release_date", "rating", "reviews_count"
    ])
    
    for product_id in range(1, 20001):
        name = f"Product {product_id}"
        category = random.choice(categories)
        price = round(random.uniform(10, 1000), 2)
        stock_quantity = random.randint(1, 500)
        supplier = random.choice(suppliers)
        description = f"Description for {name} in {category}"
        weight = round(random.uniform(0.1, 10), 2)  # Weight in kg
        dimensions = f"{random.randint(10, 100)}x{random.randint(10, 50)}x{random.randint(5, 30)}"  # Dimensions in cm
        warranty = random.randint(1, 5)  # Warranty in years
        release_date = random_date(datetime(2018, 1, 1), datetime(2023, 12, 31)).strftime("%Y-%m-%d")
        rating = round(random.uniform(3.0, 5.0), 1)  # Rating out of 5
        reviews_count = random.randint(10, 5000)  # Number of reviews
        
        # Write row
        writer.writerow([
            product_id, name, category, price, stock_quantity, supplier, description,
            weight, dimensions, warranty, release_date, rating, reviews_count
        ])

print(f"Enriched product data generated in {output_file}")