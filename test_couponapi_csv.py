import csv
import os

# Path to your downloaded CSV file
csv_path = os.path.expanduser(r"~/Downloads/incremental_4878_20250722225203.csv")

# Read and print all offers from the CSV
with open(csv_path, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    offers = list(reader)
    print(f"Total offers: {len(offers)}")
    for offer in offers[:10]:  # Print first 10 offers for inspection
        print(offer)

# You can now filter, analyze, or use these offers in memory for testing
# Example: Find all offers for Walmart
walmart_offers = [o for o in offers if 'walmart' in o.get('store', '').lower()]
print(f"Walmart offers: {len(walmart_offers)}")
for offer in walmart_offers[:5]:
    print(offer)
