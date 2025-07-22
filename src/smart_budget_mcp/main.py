# src/smart_budget_mcp/main.py
import asyncio
import os
import httpx
from fastapi import FastAPI, Query

from .state import wishlist, groceries, budget, user_profile
from .schemas import BudgetInput, CardNamesInput, WishlistItemInput, GroceryItemInput
from .savings_engine import (
    get_credit_card_perks, fetch_gift_card_deals,
    fetch_rakuten_coupons, fetch_rakuten_offers, fetch_rakuten_cashback,
    fetch_rakuten_advertisers, fetch_rakuten_products, fetch_rakuten_deeplink, fetch_rakuten_link_locator
)

# --- LLM Integration ---
try:
    import ollama
    OLLAMA_AVAILABLE = True
except ImportError:
    OLLAMA_AVAILABLE = False

app = FastAPI()

# --- Helper for API Key ---
def get_serpapi_key():
    key = os.getenv("SERPAPI_KEY")
    if not key:
        raise ValueError("SERPAPI_KEY environment variable not set.")
    return key

# --- LLM Quantity/Unit Extraction ---
async def extract_quantity_with_llm(title, price):
    if not OLLAMA_AVAILABLE:
        return None, None, None
    prompt = f"""
    Extract the total quantity, unit type, and price per unit from this product title and price.
    Title: '{title}'
    Price: {price}
    Respond in JSON: {{'total_quantity': ..., 'unit_type': ..., 'unit_price': ...}}
    """
    try:
        response = await asyncio.to_thread(
            lambda: ollama.chat(
                model='gemma3',
                messages=[{'role': 'user', 'content': prompt}],
                format='json',
                options={'temperature': 0.0}
            )
        )
        import json
        data = json.loads(response['message']['content'])
        return data.get('total_quantity'), data.get('unit_type'), data.get('unit_price')
    except Exception:
        return None, None, None

# Google Shopping Results API via SerpApi fetcher (all stores, location-aware)
async def fetch_google_shopping_prices_nearby(item_name, location, num=20):
    SERPAPI_KEY = get_serpapi_key()
    params = {
        "engine": "google_shopping",
        "q": item_name,
        "api_key": SERPAPI_KEY,
        "gl": "us",
        "hl": "en",
        "location": location,
        "num": num
    }
    url = "https://serpapi.com/search.json"
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(url, params=params)
            if resp.status_code == 200:
                data = resp.json()
                offers = []
                for section in ["inline_shopping_results", "shopping_results"]:
                    for result in data.get(section, []):
                        offer = {
                            "store": result.get("source"),
                            "title": result.get("title"),
                            "price": result.get("price"),
                            "extracted_price": result.get("extracted_price"),
                            "link": result.get("link"),
                            "delivery": result.get("delivery"),
                            "extensions": result.get("extensions"),
                            "thumbnail": result.get("thumbnail"),
                        }
                        offers.append(offer)
                return offers
            return []
    except Exception:
        return []

@app.post("/budget")
async def set_user_budget(data: BudgetInput):
    budget["monthly_limit"] = data.monthly_limit
    return {"message": f"Budget successfully set to ${data.monthly_limit} per month."}

@app.post("/wishlist/items")
async def add_user_wishlist_item(data: WishlistItemInput):
    wishlist.append({"name": data.name, "urgency": data.urgency})
    return {"message": f"'{data.name}' added to wishlist.", "current_wishlist": wishlist}

@app.post("/groceries/items")
async def add_user_grocery_item(data: GroceryItemInput):
    groceries.append({
        "name": data.name, 
        "quantity": data.quantity, 
        "frequency": data.frequency
    })
    return {"message": f"'{data.name}' added to grocery list.", "current_groceries": groceries}

@app.post("/profile/cards")
async def set_user_credit_cards(data: CardNamesInput):
    user_profile["credit_cards"] = data.card_names
    return {"message": "Credit cards updated successfully.", "current_cards": user_profile["credit_cards"]}

@app.get("/shopping_list_value")
async def get_shopping_list_value(items: list[str] = Query(...), location: str = Query(...), num: int = Query(10)):
    all_items_in_memory = wishlist + groceries
    item_dicts = []
    for name in items:
        found = next((item for item in all_items_in_memory if item.get("name", "").lower() == name.lower()), None)
        item_dicts.append(found or {"name": name})

    results = {}
    for item in item_dicts:
        item_name = item["name"]
        offers = await fetch_google_shopping_prices_nearby(item_name, location, num)
        analyzed_offers = []
        best_deal = None
        best_effective_price = float('inf')
        for offer in offers:
            base_price = offer.get("extracted_price")
            if base_price is None:
                continue
            try:
                base_price = float(base_price)
            except Exception:
                continue
            # --- LLM Quantity/Unit Extraction ---
            total_quantity, unit_type, unit_price = await extract_quantity_with_llm(offer.get("title", ""), base_price)
            # --- Rakuten Integrations ---
            rakuten_coupons = await fetch_rakuten_coupons(offer.get("store", ""))
            rakuten_offers = await fetch_rakuten_offers(offer.get("store", ""))
            rakuten_cashback = await fetch_rakuten_cashback(offer.get("store", ""))
            rakuten_advertisers = await fetch_rakuten_advertisers(store_name=offer.get("store", ""))
            rakuten_products = await fetch_rakuten_products(item_name, None)
            rakuten_deeplink = await fetch_rakuten_deeplink([offer.get("link", "")])
            rakuten_link_locator = await fetch_rakuten_link_locator(advertiser_name=offer.get("store", ""))
            # Apply gift card deals
            gift_card = await fetch_gift_card_deals(offer.get("store", ""))
            gift_card_discount = gift_card["discount"] if gift_card else 0.0
            # Apply credit card perks
            perks = get_credit_card_perks(offer.get("store", ""), user_profile["credit_cards"])
            best_perk = max([p["value"] for p in perks], default=0.0)
            price_after_gift_card = base_price * (1 - gift_card_discount)
            price_after_perks = price_after_gift_card * (1 - best_perk)
            analyzed = {
                **offer,
                "base_price": base_price,
                "gift_card_discount": gift_card_discount,
                "price_after_gift_card": round(price_after_gift_card, 2),
                "credit_card_perk": best_perk,
                "final_effective_price": round(price_after_perks, 2),
                "savings_breakdown": {
                    "gift_card": f"{int(gift_card_discount*100)}% off" if gift_card else None,
                    "credit_card": f"{int(best_perk*100)}% off" if best_perk else None
                },
                "llm_total_quantity": total_quantity,
                "llm_unit_type": unit_type,
                "llm_unit_price": unit_price,
                "rakuten_coupons": rakuten_coupons,
                "rakuten_offers": rakuten_offers,
                "rakuten_cashback": rakuten_cashback,
                "rakuten_advertisers": rakuten_advertisers,
                "rakuten_products": rakuten_products,
                "rakuten_deeplink": rakuten_deeplink,
                "rakuten_link_locator": rakuten_link_locator
            }
            analyzed_offers.append(analyzed)
            if price_after_perks < best_effective_price:
                best_effective_price = price_after_perks
                best_deal = analyzed
        results[item_name] = {
            "best_deal": best_deal,
            "all_deals": analyzed_offers
        }
    return results 