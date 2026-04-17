import requests
import time
import schedule

WEBHOOK_URL = "https://discord.com/api/webhooks/1494419687243644938/G2_Fj5bh69X6qS98YplRImZmcKs1FZV5fJm8JskCKjxuLSbGVSgKrXIptjJxC5UH7T1r"

USD_TO_AUD = 1.55
BASE_URL = "https://www.cheapshark.com/api/1.0/deals"

STORE_IDS = ["1", "25"]  # Steam + Epic


# ----------------------------
# Discord sender
# ----------------------------
def send_discord(message):
    try:
        requests.post(WEBHOOK_URL, json={"content": message})
    except Exception as e:
        print("Discord error:", e)


# ----------------------------
# TEST MESSAGE (SAFE)
# ----------------------------
send_discord("✅ TEST MESSAGE - BOT DEPLOYED SUCCESSFULLY")


# ----------------------------
# Convert USD → AUD
# ----------------------------
def to_aud(usd):
    return round(float(usd) * USD_TO_AUD, 2)


# ----------------------------
# Deal checker
# ----------------------------
def check_deals():
    print("🔎 Checking deals...")

    for store in STORE_IDS:
        res = requests.get(BASE_URL, params={
            "storeID": store,
            "sortBy": "savings",
            "pageSize": 30
        })

        if res.status_code != 200:
            continue

        deals = res.json()

        for game in deals:
            savings = float(game["savings"])

            # 🎯 ONLY 50–70%
            if savings < 50 or savings > 70:
                continue

            title = game["title"]
            sale = float(game["salePrice"])
            normal = float(game["normalPrice"])
            deal_id = game["dealID"]

            sale_aud = to_aud(sale)

            store_name = "Steam" if store == "1" else "Epic"

            message = (
                f"🎮 **{title}** ({store_name})\n"
                f"💰 ${sale} USD (~${sale_aud} AUD)\n"
                f"~~${normal}~~ (-{savings:.0f}%)\n"
                f"🔗 https://www.cheapshark.com/redirect?dealID={deal_id}"
            )

            send_discord(message)
            time.sleep(1)


# ----------------------------
# STARTUP
# ----------------------------
send_discord("🔥 BOT ONLINE - DAILY DEAL SCANNER")

check_deals()


# ----------------------------
# RUN DAILY
# ----------------------------
schedule.every(24).hours.do(check_deals)

print("🤖 Running 24/7...")

while True:
    schedule.run_pending()
    time.sleep(60)