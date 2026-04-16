import requests
import time

STEAM_API = "https://www.cheapshark.com/api/1.0/deals"
EPIC_API = "https://store-site-backend-static.ak.epicgames.com/freeGamesPromotions?locale=en-US&country=AU&allowCountries=AU"

seen_steam = set()
seen_epic = set()


# ---------------- STEAM ----------------
def fetch_steam():
    try:
        res = requests.get(
            STEAM_API,
            params={
                "storeID": 1,
                "pageSize": 30,
                "sortBy": "Savings",
                "desc": 1
            },
            timeout=10
        )
        res.raise_for_status()
        return res.json()
    except Exception as e:
        print("Steam API error:", e)
        return []


def process_steam(data):
    print("\n🔥 STEAM DEALS (20%+ only)")

    found = 0

    for d in data:
        try:
            savings = float(d.get("savings", 0))

            # 🔥 filter junk
            if savings < 20:
                continue

            deal_id = d.get("dealID")
            if deal_id in seen_steam:
                continue

            seen_steam.add(deal_id)

            print(f"{d.get('title')} | ${d.get('salePrice')} (was ${d.get('normalPrice')}) - {round(savings)}% OFF")

            found += 1

        except:
            continue

    if found == 0:
        print("No strong Steam deals right now")


# ---------------- EPIC ----------------
def fetch_epic():
    try:
        res = requests.get(EPIC_API, timeout=10)
        res.raise_for_status()
        return res.json()
    except Exception as e:
        print("Epic API error:", e)
        return {}


def process_epic(data):
    print("\n🎮 EPIC FREE GAMES")

    games = data.get("data", {}).get("Catalog", {}).get("searchStore", {}).get("elements", [])

    found = 0

    for g in games:
        try:
            title = g.get("title")
            gid = g.get("id")

            if not title or not gid:
                continue

            if gid in seen_epic:
                continue

            seen_epic.add(gid)

            print(f"🎁 {title}")
            found += 1

        except:
            continue

    if found == 0:
        print("No new Epic freebies")


# ---------------- MAIN ----------------
def main():
    print("🚀 Deal Bot Running (Clean Mode)\n")

    while True:
        steam = fetch_steam()
        process_steam(steam)

        epic = fetch_epic()
        process_epic(epic)

        print("\nSleeping 5 minutes...\n")
        time.sleep(300)


if __name__ == "__main__":
    main()