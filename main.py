import requests
import time
import schedule
import os

WEBHOOK_URL = os.getenv("WEBHOOK_URL")

USD_TO_AUD = 1.55

BASE_URL = "https://www.cheapshark.com/api/1.0/deals"


def to_aud(usd):
    return round(float(usd) * USD_TO_AUD, 2)


def send_discord(msg):
    if not WEBHOOK_URL:
        print("No webhook set")
        return

    try:
        requests.post(WEBHOOK_URL, json={"content": msg})
    except Exception as e:
        print("Discord error:", e)


def check_deals():
    print("Checking deals...")

    res = requests.get(BASE_URL, params={
        "sortBy": "price",
        "pageSize": 5
    })

    if res.status_code != 200:
        print("API error")
        return

    deals = res.json()

    for game in deals:
        title = game["title"]
        sale = float(game["salePrice"])
        normal = float(game["normalPrice"])
        savings = float(game["savings"])
        deal_id = game["dealID"]

        msg = (
            f"🎮 {title}\n"
            f"💰 ${sale} USD (~${to_aud(sale)} AUD)\n"
            f"~~${normal}~~ (-{savings:.0f}%)\n"
            f"https://www.cheapshark.com/redirect?dealID={deal_id}"
        )

        send_discord(msg)
        time.sleep(2)


# run once immediately
check_deals()

# schedule every 5 hours
schedule.every(5).hours.do(check_deals)

print("Bot running...")

while True:
    schedule.run_pending()
    time.sleep(60)