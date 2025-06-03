import json

with open('database/data/dealerships.json', 'r') as f:
    data = json.load(f)

fixture = []
for item in data['dealerships']:
    fixture.append({
        "model": "djangoapp.dealer",  # Use your app and model name
        "pk": item["id"],
        "fields": {
            "full_name": item["full_name"],
            "city": item["city"],
            "address": item["address"],
            "zip": item["zip"],
            "state": item["state"]
        }
    })

with open('database/data/dealerships_fixture.json', 'w') as f:
    json.dump(fixture, f, indent=2)

print("Fixture created: database/data/dealerships_fixture.json")