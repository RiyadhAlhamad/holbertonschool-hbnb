
import requests

base_url = "http://127.0.0.1:5000/api/v1/"

# -------------------- USERS --------------------
print("---- USERS ----")
users_url = base_url + "users/"
users_data = [
    {"first_name": "Riyadh", "last_name": "Alhamad", "email": "riyadh@mail.com", "password": "1234"},
    {"first_name": "Mhamad", "last_name": "Alhamad", "email": "mhamad@mail.com", "password": "1234"},
    {"first_name": "Badr", "last_name": "Alamri", "email": "badr@mail.com", "password": "1234"},
    {"first_name": "Duplicate", "last_name": "User", "email": "riyadh@mail.com", "password": "1234"}  # Duplicate email
]

user_ids = []
tokens = []

for user in users_data:
    res = requests.post(users_url, json=user)
    print(f"POST {user['email']} →", res.status_code, res.json())
    if res.status_code == 201:
        login = requests.post(base_url + "auth/login", json={
            "email": user["email"],
            "password": user["password"]
        })
        token = login.json().get("access_token")
        if token:
            tokens.append(token)
        user_ids.append(res.json()["id"])

# -------------------- AMENITIES --------------------
print("\n---- AMENITIES ----")
amenities_url = base_url + "amenities/"
amenities_data = [
    {"name": "Wi-Fi"},
    {"name": "Pool"},
    {"name": "Parking"}
]
amenity_ids = []

for amenity in amenities_data:
    res = requests.post(amenities_url, json=amenity)
    print(f"POST {amenity['name']} →", res.status_code, res.json())
    if res.status_code == 201:
        amenity_ids.append(res.json()["id"])

# -------------------- PLACES --------------------
print("\n---- PLACES ----")
places_url = base_url + "places/"
place_ids = []

places_data = [
    {
        "title": "Beach House",
        "description": "A beautiful house by the sea",
        "price": 250.0,
        "latitude": 24.7136,
        "longitude": 46.6753,
        "amenities": amenity_ids[:2]
    },
    {
        "title": "City Apartment",
        "description": "A cozy apartment in downtown",
        "price": 150.0,
        "latitude": 21.3891,
        "longitude": 39.8579,
        "amenities": amenity_ids[1:]
    }
]

for i, place in enumerate(places_data):
    headers = {"Authorization": f"Bearer {tokens[i]}"}
    res = requests.post(places_url, json=place, headers=headers)
    try:
        response_data = res.json()
        print(f"POST {place['title']} →", res.status_code, response_data)
        place_id = response_data.get("id") or response_data.get("Place id")
        if place_id:
            place_ids.append(place_id)
    except Exception as e:
        print("Failed to parse place response:", e)
        print("Raw response:", res.text)

# -------------------- REVIEWS --------------------
print("\n---- REVIEWS ----")
reviews_url = base_url + "reviews/"
if user_ids and place_ids:
    review_data = {
        "text": "Absolutely loved this place!",
        "rating": 5,
        "place_id": place_ids[0]
    }
    headers = {"Authorization": f"Bearer {tokens[0]}"}
    res = requests.post(reviews_url, json=review_data, headers=headers)
    print("POST Review →", res.status_code)
    try:
        print(res.json())
    except Exception as e:
        print("Failed to parse review:", e)
        print("Raw response:", res.text)
