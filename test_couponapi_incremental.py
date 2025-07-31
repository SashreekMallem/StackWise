import requests
import time

API_KEY = "d51f3dbccbc971044a8ea9f6dc7c0526"
# 1 year ago from now
one_year_ago = int(time.time()) - 365 * 24 * 60 * 60
url = f"https://couponapi.org/api/getIncrementalFeed/?API_KEY={API_KEY}&last_extract={one_year_ago}&format=json"

print(f"Requesting incremental feed since: {one_year_ago} (UNIX timestamp)")
resp = requests.get(url)
data = resp.json()

if data.get("result"):
    offers = data.get("offers", [])
    print(f"Received {len(offers)} offers since 1 year ago.")
    for offer in offers[:10]:  # Print first 10 offers for inspection
        print(offer)
else:
    print("Error:", data.get("error"))
