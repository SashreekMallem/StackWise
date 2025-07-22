import httpx
import asyncio
import os

# --- Rakuten API Key ---
RAKUTEN_API_KEY = os.getenv("RAKUTEN_API_KEY")

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

# --- Rakuten API Integrations ---

async def fetch_rakuten_coupons(store_name):
    if not RAKUTEN_API_KEY:
        return []
    url = "https://api.rakuten.com/coupon/1.0"
    params = {"merchant": store_name, "api_key": RAKUTEN_API_KEY}
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(url, params=params)
            if resp.status_code == 200:
                return resp.json()
    except Exception:
        pass
    return []

async def fetch_rakuten_offers(store_name):
    if not RAKUTEN_API_KEY:
        return []
    url = "https://api.rakuten.com/v1/offers"
    params = {"merchant": store_name, "api_key": RAKUTEN_API_KEY}
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(url, params=params)
            if resp.status_code == 200:
                return resp.json()
    except Exception:
        pass
    return []

async def fetch_rakuten_cashback(store_name):
    if not RAKUTEN_API_KEY:
        return None
    url = "https://api.rakuten.com/v1/partnerships"
    params = {"merchant": store_name, "api_key": RAKUTEN_API_KEY}
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(url, params=params)
            if resp.status_code == 200:
                return resp.json()
    except Exception:
        pass
    return None

async def fetch_rakuten_advertisers(store_name=None, advertiser_id=None):
    if not RAKUTEN_API_KEY:
        return []
    if advertiser_id:
        url = f"https://api.rakuten.com/v2/advertisers/{advertiser_id}"
        params = {"api_key": RAKUTEN_API_KEY}
    else:
        url = "https://api.rakuten.com/v2/advertisers"
        params = {"name": store_name, "api_key": RAKUTEN_API_KEY} if store_name else {"api_key": RAKUTEN_API_KEY}
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(url, params=params)
            if resp.status_code == 200:
                return resp.json()
    except Exception:
        pass
    return []

async def fetch_rakuten_products(query, advertiser_id=None):
    if not RAKUTEN_API_KEY:
        return []
    url = "https://api.rakuten.com/productsearch/1.0"
    params = {"query": query, "api_key": RAKUTEN_API_KEY}
    if advertiser_id:
        params["advertiser_id"] = advertiser_id
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(url, params=params)
            if resp.status_code == 200:
                return resp.json()
    except Exception:
        pass
    return []

async def fetch_rakuten_deeplink(urls):
    if not RAKUTEN_API_KEY:
        return []
    url = "https://api.rakuten.com/v1/links/deep_links"
    headers = {"Authorization": f"Bearer {RAKUTEN_API_KEY}"}
    data = {"urls": urls}
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.post(url, headers=headers, json=data)
            if resp.status_code == 200:
                return resp.json()
    except Exception:
        pass
    return []

async def fetch_rakuten_link_locator(advertiser_name=None, advertiser_id=None, category_id=None):
    if not RAKUTEN_API_KEY:
        return []
    base = "https://api.rakuten.com/linklocator/1.0"
    if advertiser_name:
        url = f"{base}/getMerchByName/{advertiser_name}"
    elif advertiser_id:
        url = f"{base}/getMerchByID/{advertiser_id}"
    elif category_id:
        url = f"{base}/getMerchByCategory/{category_id}"
    else:
        return []
    params = {"api_key": RAKUTEN_API_KEY}
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(url, params=params)
            if resp.status_code == 200:
                return resp.json()
    except Exception:
        pass
    return []

