import requests
import json
import os
import schedule
import time
from datetime import datetime
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

PRODUCT_URL = "https://www.amazon.com/dp/B07RTQ4VM7"
PRODUCT_NAME = "Afnan Men Eau de Parfum 3.4oz"
TARGET_PRICE = 20
PRICE_HISTORY_FILE = "price_history.json"

def get_price():
    
    
    SCRAPER_API_KEY = os.getenv("SCRAPER_API_KEY")
    
    
    scraper_url = f"http://api.scraperapi.com?api_key={SCRAPER_API_KEY}&url={PRODUCT_URL}"

    try:
        response = requests.get(scraper_url, timeout=60)
        soup = BeautifulSoup(response.content, "lxml")

        price_element = (
            soup.find("span", {"class": "a-price-whole"}) or
            soup.find("span", {"id": "priceblock_ourprice"}) or
            soup.find("span", {"id": "priceblock_dealprice"})
        )

        if price_element:
            raw = price_element.get_text()
            price = float(raw.replace(",", "").replace(".", "").strip())
            return price
        else:
            print("❌ Could not find price on page.")
            return None

    except Exception as e:
        print(f"❌ Error scraping: {e}")
        return None

def save_price(price):
    if os.path.exists(PRICE_HISTORY_FILE):
        with open(PRICE_HISTORY_FILE, "r") as f:
            history = json.load(f)
    else:
        history = []

    entry = {
        "price": price,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    history.append(entry)

    with open(PRICE_HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=2)

    print(f"💾 Price ₹{price} saved to history.")

def get_price_history():
    if os.path.exists(PRICE_HISTORY_FILE):
        with open(PRICE_HISTORY_FILE, "r") as f:
            return json.load(f)
    return []

def send_alert(current_price, previous_price=None):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

    message = "🚨 *PRICE DROP ALERT!*\n"
    message += "━━━━━━━━━━━━━━━━━━━━\n\n"
    message += f"🛒 *Product:* {PRODUCT_NAME}\n"
    message += f"💰 *Current Price:* ₹{current_price:,}\n"
    message += f"🎯 *Your Target:* ₹{TARGET_PRICE:,}\n"

    if previous_price:
        saved = previous_price - current_price
        message += f"📉 *Price Drop:* ₹{saved:,} less than before!\n"

    message += f"\n🔗 [Buy Now]({PRODUCT_URL})\n"
    message += "\n━━━━━━━━━━━━━━━━━━━━\n"
    message += "🤖 _Sent by your Price Tracker Bot_"

    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "Markdown",
        "disable_web_page_preview": True,
    }

    response = requests.post(url, json=payload)
    if response.status_code == 200:
        print("✅ Alert sent to Telegram!")
    else:
        print(f"❌ Failed to send alert: {response.text}")

def send_status_update(current_price):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

    history = get_price_history()
    highest = max(h["price"] for h in history) if history else current_price
    lowest = min(h["price"] for h in history) if history else current_price

    message = "📊 *PRICE CHECK UPDATE*\n"
    message += "━━━━━━━━━━━━━━━━━━━━\n\n"
    message += f"🛒 *Product:* {PRODUCT_NAME}\n"
    message += f"💰 *Current Price:* ₹{current_price:,}\n"
    message += f"🎯 *Your Target:* ₹{TARGET_PRICE:,}\n\n"
    message += f"📈 *Highest Seen:* ₹{highest:,}\n"
    message += f"📉 *Lowest Seen:* ₹{lowest:,}\n"
    message += f"🔢 *Checks Done:* {len(history)}\n\n"

    if current_price > TARGET_PRICE:
        diff = current_price - TARGET_PRICE
        message += f"⏳ _Still ₹{diff:,} above your target. Waiting..._\n"

    message += "\n━━━━━━━━━━━━━━━━━━━━\n"
    message += "🤖 _Sent by your Price Tracker Bot_"

    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "Markdown",
        "disable_web_page_preview": True,
    }

    requests.post(url, json=payload)
    print("📊 Status update sent.")

def check_price():
    print(f"\n⏰ Checking price at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    current_price = get_price()

    if current_price is None:
        print("⚠️  Skipping this check — could not get price.")
        return

    print(f"💰 Current price: ₹{current_price:,}")
    print(f"🎯 Target price:  ₹{TARGET_PRICE:,}")

    history = get_price_history()
    previous_price = history[-1]["price"] if history else None

    save_price(current_price)

    if current_price <= TARGET_PRICE:
        print("🚨 Target reached! Sending alert...")
        send_alert(current_price, previous_price)
    else:
        print("⏳ Price still above target. Sending status update...")
        send_status_update(current_price)

if __name__ == "__main__":
    print("🛒 Price Tracker Bot started!")
    print(f"   Product : {PRODUCT_NAME}")
    print(f"   URL     : {PRODUCT_URL}")
    print(f"   Target  : ₹{TARGET_PRICE:,}")
    print()

    check_price()

    schedule.every(6).hours.do(check_price)

    print("\n⏰ Scheduled to check every 6 hours. Bot is running...")

    while True:
        schedule.run_pending()
        time.sleep(60)