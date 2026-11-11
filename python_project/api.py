import requests

API_URL = "https://rest-api-test-self.vercel.app/api/3"


def get_rest_api_data() -> list[dict[str, object]]:
    data = requests.get(API_URL, timeout=10).json()
    return [
        {
            "ID": person.get("id"),
            "EMAIL": person.get("email"),
            "ZIPCODE": person["address"].get("zipcode"),
            "LAT": person["address"]["geo"].get("lat"),
            "LNG": person["address"]["geo"].get("lng"),
        }
        for person in data
    ]
