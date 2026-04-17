import requests
import time
import schedule
import matplotlib.pyplot as plt

WEBHOOK_URL = "https://discord.com/api/webhooks/1494419687243644938/G2_Fj5bh69X6qS98YplRImZmcKs1FZV5fJm8JskCKjxuLSbGVSgKrXIptjJxC5UH7T1r"

USD_TO_AUD = 1.55

BASE_URL = "https://www.cheapshark.com/api/1.0/deals"
GAME_INFO_URL = "https://www.cheapshark.com/api/1.0/games"


# ----------------------------
# Discord sender
# ----------------------------
def send_discord(msg, file=None):
    try:
        if file:
            with open(file, "rb") as f:
                requests.post(
                    WEBHOOK_URL,
                    data={"content": msg},
                    files={"file": f}
                )
        else:
            requests.post(WEBHOOK_URL, json={"content": msg})
    except Exception as e:
        print("Discord error:", e)


# ----------------------------
# TEST MESSAGE (IMPORTANT)
# ----------------------------
def test_webhook():
    print("Sending test webhook...")
    send_discord("🔥 BOT IS ONLINE (TEST MESSAGE)")


# ----------------------------
# Convert currency
# ----------------------------
def to_aud(usd):
    return round(float(usd) * USD_TO_AUD, 2)


# ----------------------------
# Get deals
# ----------------------------
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

        sale_aud = to_aud(sale)

        msg = (
            f"🎮 **{title}**\n"
            f"💰 ${sale} USD (~${sale_aud} AUD)\n"
            f"~~${normal}~~ (-{savings:.0f}%)\n"
            f"🔗 https://www.cheapshark.com/redirect?dealID={deal_id}"
        )

        send_discord(msg)
        time.sleep(2)


# ----------------------------
# RUN ON START
# ----------------------------
test_webhook()   # 🔥 THIS IS THE IMPORTANT PART

check_deals()


# ----------------------------
# SCHEDULE (every 5 hours)
# ----------------------------
schedule.every(5).hours.do(check_deals)

print("Bot running...")

while True:
    schedule.run_pending()
    time.sleep(60)