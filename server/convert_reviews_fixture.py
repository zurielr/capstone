import json
from datetime import datetime

with open('database/data/reviews.json', 'r') as f:
    data = json.load(f)

fixture = []
for item in data['reviews']:
    purchase_date = item.get("purchase_date")
    if purchase_date:
        try:
            purchase_date = datetime.strptime(purchase_date, "%m/%d/%Y").strftime("%Y-%m-%d")
        except Exception:
            purchase_date = None
    else:
        purchase_date = None

    fixture.append({
        "model": "djangoapp.review",
        "pk": item["id"],
        "fields": {
            "name": item["name"],
            "dealership": item["dealership"],
            "review": item["review"],
            "purchase": item["purchase"],
            "purchase_date": purchase_date,
            # "car": ???  # You must map this to a valid CarModel PK if you want to set it
            # "sentiment": "neutral"  # Optional, if you want to set it
        }
    })

with open('database/data/reviews_fixture.json', 'w') as f:
    json.dump(fixture, f, indent=2)

print("Fixture created: database/data/reviews_fixture.json")