import requests
import time

def fetch_deals():
    try:
        print("Checking deals...")
        
        response = requests.get(
            "YOUR_API_URL_HERE",
            timeout=10
        )

        response.raise_for_status()  # catches bad HTTP codes

        data = response.json()

        print("Deals fetched successfully")
        return data

    except requests.exceptions.RequestException as e:
        print("API request failed:", e)
        return None

    except ValueError as e:
        print("JSON decode failed:", e)
        return None

    except Exception as e:
        print("Unexpected error:", e)
        return None