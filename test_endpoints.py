import requests
import json

BASE = "http://127.0.0.1:8000"

def print_result(name, resp):
    print(f"\n=== {name} ===")
    print(f"Status: {resp.status_code}")
    try:
        print(json.dumps(resp.json(), indent=2))
    except Exception:
        print(resp.text)
    print("PASS" if resp.ok else "FAIL")

# 1. Test /profile/cards
resp = requests.post(f"{BASE}/profile/cards", json={"card_names": ["Target RedCard", "Chase Freedom"]})
print_result("POST /profile/cards", resp)

# 2. Test /budget
resp = requests.post(f"{BASE}/budget", json={"monthly_limit": 2500})
print_result("POST /budget", resp)

# 3. Test /wishlist/items
resp = requests.post(f"{BASE}/wishlist/items", json={"name": "iPhone 15", "urgency": "high"})
print_result("POST /wishlist/items", resp)

# 4. Test /groceries/items
resp = requests.post(f"{BASE}/groceries/items", json={"name": "milk", "quantity": 2, "frequency": "weekly"})
print_result("POST /groceries/items", resp)

# 5. Test /shopping_list_value
resp = requests.get(f"{BASE}/shopping_list_value", params={"items": ["milk"], "location": "Seattle", "num": 2})
print_result("GET /shopping_list_value", resp) 