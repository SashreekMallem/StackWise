import httpx
import asyncio
import os


# --- Load API keys from .env ---
from dotenv import load_dotenv
load_dotenv()
COUPONSAPI_KEY = os.getenv("COUPONSAPI_KEY")

# --- Layer 3: Mock Credit Card Perks ---
# In a real application, this would be a database populated by a service like RewardsCC API
# or a user's own input. For now, we mock it.
mock_credit_card_offers = {
    "Chase Freedom": {"perks": [{"category": "groceries", "value": 0.05, "type": "cashback"}]},
    "Amex Gold": {"perks": [{"category": "restaurants", "value": 0.04, "type": "cashback"}]},
    "Target RedCard": {"perks": [{"store": "Target", "value": 0.05, "type": "discount"}]},
    "Walmart Capital One": {"perks": [{"store": "Walmart", "value": 0.05, "type": "cashback"}]}
}

# We need a way to map stores to categories. This is a simplified version.
store_to_category_map = {
    "instacart": "groceries",
    "qfc": "groceries",
    "safeway": "groceries",
    "fred meyer": "groceries",
    "postmates": "restaurants",
    "uber eats": "restaurants",
    "citarella": "groceries",
    "target": "retail",
    "walmart": "retail",
}

def get_credit_card_perks(store_name: str, user_cards: list[str]) -> list[dict]:
    """
    Checks for credit card perks for a given store from a user's list of cards.
    
    Args:
        store_name: The name of the store (e.g., "Target").
        user_cards: A list of card names the user has (e.g., ["Chase Freedom", "Target RedCard"]).

    Returns:
        A list of perk dictionaries that apply.
    """
    applicable_perks = []
    if not store_name:
        return applicable_perks

    store_name_lower = store_name.lower()
    category = store_to_category_map.get(store_name_lower)

    for card_name in user_cards:
        if card_name in mock_credit_card_offers:
            for perk in mock_credit_card_offers[card_name]["perks"]:
                # Check for store-specific perks
                if perk.get("store", "").lower() == store_name_lower:
                    applicable_perks.append({"card": card_name, **perk})
                # Check for category-specific perks
                elif perk.get("category") == category:
                    applicable_perks.append({"card": card_name, **perk})
    
    return applicable_perks


# --- Layer 1: Discounted Gift Cards (Placeholder) ---

async def fetch_gift_card_deals(store_name: str):
    """
    (Placeholder) Fetches discounted gift card deals from an API like Reloadly.
    
    For now, it will return a mock deal for specific stores.
    """
    # In a real implementation, you would use httpx to call the Reloadly API
    # with your credentials.
    # e.g., GET https://api.reloadly.com/discounts
    
    mock_deals = {
        "target": {"discount": 0.04, "provider": "Reloadly"}, # 4% off
        "starbucks": {"discount": 0.07, "provider": "Reloadly"} # 7% off
    }

    if store_name and store_name.lower() in mock_deals:
        return mock_deals[store_name.lower()]
    
    return None

# --- CouponsAPI.org Integrations ---


# --- CouponAPI.org Incremental Feed Integration ---
import requests
import time

def fetch_couponapi_incremental(last_extract=None):
    """
    Fetches incremental coupon feed from CouponAPI.org since last_extract (UNIX timestamp).
    Returns a list of offers.
    """
    if not COUPONSAPI_KEY:
        return []
    if last_extract is None:
        # Default: 1 year ago
        last_extract = int(time.time()) - 365 * 24 * 60 * 60
    url = f"https://couponapi.org/api/getIncrementalFeed/?API_KEY={COUPONSAPI_KEY}&last_extract={last_extract}&format=json"
    try:
        resp = requests.get(url)
        data = resp.json()
        if data.get("result"):
            return data.get("offers", [])
    except Exception:
        pass
    return []

