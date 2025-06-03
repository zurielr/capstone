import json

with open('database/data/car_records.json', 'r') as f:
    data = json.load(f)

fixture = []
DEFAULT_CAR_MAKE_PK = 1  # Change this to the correct CarMake PK

for idx, item in enumerate(data['cars'], start=1):
    fixture.append({
        "model": "djangoapp.carmodel",
        "pk": idx,
        "fields": {
            "car_make": DEFAULT_CAR_MAKE_PK,  # <-- REQUIRED!
            "dealer": item.get("dealer_id"),  # FK to Dealer, or None
            "name": item["model"],
            "type": item.get("type", "SUV"),  # or set a default
            "body_type": item.get("bodyType", "Unknown"),
            "year": item.get("year", 2023),
            "mileage": item.get("mileage", 0),
        }
    })

with open('database/data/car_records_fixture.json', 'w') as f:
    json.dump(fixture, f, indent=2)

print("Fixture created: database/data/car_records_fixture.json")