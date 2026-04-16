import requests
import time

# ---------------- CONFIG ----------------
STEAM_API = "https://www.cheapshark.com/api/1.0/deals"
EPIC_API = "https://store-site-backend-static.ak.epicgames.com/freeGamesPromotions?locale=en-US&country=AU&allowCountries=AU"

DISCORD_WEBHOOK = "https://discord.com/api/webhooks/1494419687243644938/G2_Fj5bh69X6qS98YplRImZmcKs1FZV5fJm8JskCKjxuLSbGVSgKrXIptjJxC5UH7T1r"

sent_ids = set()


# ---------------- DISCORD ----------------
def send_discord(title, description, color=0x00ff99):
    if not DISCORD_WEBHOOK:
        return

    payload = {
        "embeds": [
            {
                "title": title,
                "description": description,
                "color": color
            }
        ]
    }

    try:
        requests.post(DISCORD_WEBHOOK, json=payload)
    except Exception as e:
        print("Discord error:", e)


# ---------------- STEAM ----------------
def fetch_steam():
    try:
        res = requests.get(
            STEAM_API,
            params={
                "storeID": 1,
                "pageSize": 20,
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
    print("\n🔥 STEAM DEALS")

    for d in data:
        try:
            deal_id = d.get("dealID")

            if deal_id in sent_ids:
                continue

            savings = float(d.get("savings", 0))

            if savings < 20:
                continue

            sent_ids.add(deal_id)

            msg = (
                f"💰 **{d.get('title')}**\n"
                f"${d.get('salePrice')} (was ${d.get('normalPrice')})\n"
                f"🔥 {round(savings)}% OFF"
            )

            print(msg)
            send_discord("🔥 Steam Deal", msg, 0x1abc9c)

        except Exception as e:
            print("Steam parse error:", e)


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

    for g in games:
        try:
            gid = g.get("id")
            title = g.get("title")

            if not gid or gid in sent_ids:
                continue

            price = g.get("price", {}).get("totalPrice", {}).get("fmtPrice", {}).get("originalPrice", "")

            if price not in ["0", "0.00", "FREE"]:
                continue

            sent_ids.add(gid)

            msg = f"🎁 **FREE EPIC GAME**\n{title}"

            print(msg)
            send_discord("🎮 Epic Free Game", msg, 0x5865f2)

        except Exception as e:
            print("Epic parse error:", e)


# ---------------- MAIN LOOP ----------------
def main():
    print("🚀 Deal Bot Started (Full Discord Version)\n")

    while True:
        steam = fetch_steam()
        process_steam(steam)

        epic = fetch_epic()
        process_epic(epic)

        print("\nSleeping 5 minutes...\n")
        time.sleep(300)


if __name__ == "__main__":
    main()