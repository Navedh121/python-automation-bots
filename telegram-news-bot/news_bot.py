import requests
import schedule
import time
import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

def fetch_general_news():
    url = "https://newsapi.org/v2/top-headlines"
    params = {
        "apiKey": NEWS_API_KEY,
        "language": "en",
        "pageSize": 5,
        "category": "general",
    }
    response = requests.get(url, params=params)
    data = response.json()
    return data.get("articles", [])

def fetch_tech_news():
    url = "https://newsapi.org/v2/top-headlines"
    params = {
        "apiKey": NEWS_API_KEY,
        "language": "en",
        "pageSize": 5,
        "category": "technology",
    }
    response = requests.get(url, params=params)
    data = response.json()
    return data.get("articles", [])

def fetch_sports_news():
    url = "https://newsapi.org/v2/top-headlines"
    params = {
        "apiKey": NEWS_API_KEY,
        "language": "en",
        "pageSize": 5,
        "category": "sports",
    }
    response = requests.get(url, params=params)
    data = response.json()
    return data.get("articles", [])

def fetch_ai_news():
    url = "https://newsapi.org/v2/everything"
    params = {
        "apiKey": NEWS_API_KEY,
        "language": "en",
        "pageSize": 5,
        "q": "artificial intelligence OR ChatGPT OR OpenAI OR Gemini OR LLM",
        "sortBy": "publishedAt",
    }
    response = requests.get(url, params=params)
    data = response.json()
    return data.get("articles", [])

def format_section(title, emoji, articles, empty_msg):
    block = f"{emoji} *{title}*\n"
    block += "━━━━━━━━━━━━━━━━━━━━\n"

    if articles:
        for i, article in enumerate(articles, 1):
            headline = article.get("title", "No title")
            source = article.get("source", {}).get("name", "Unknown")
            url = article.get("url", "")

            if " - " in headline:
                headline = headline.rsplit(" - ", 1)[0]

            block += f"\n*{i}.* {headline}\n"
            block += f"   📡 _{source}_\n"
            block += f"   🔗 [Read more]({url})\n"
    else:
        block += f"\n_{empty_msg}_\n"

    return block

def format_news_message(general_articles, tech_articles, sports_articles, ai_articles):
    message = "🌍 *DAILY NEWS DIGEST*\n"
    message += "━━━━━━━━━━━━━━━━━━━━\n\n"

    message += format_section("GENERAL & WORLD NEWS", "📰", general_articles, "No general news available right now.")
    message += "\n"
    message += format_section("TECH NEWS", "💻", tech_articles, "No tech news available right now.")
    message += "\n"
    message += format_section("SPORTS NEWS", "⚽", sports_articles, "No sports news available right now.")
    message += "\n"
    message += format_section("AI NEWS", "🤖", ai_articles, "No AI news available right now.")

    message += "\n━━━━━━━━━━━━━━━━━━━━\n"
    message += "🤖 _Sent by your NewsBot_"

    return message

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "Markdown",
        "disable_web_page_preview": True,
    }
    response = requests.post(url, json=payload)

    if response.status_code == 200:
        print("✅ News sent to Telegram successfully!")
    else:
        print(f"❌ Failed to send. Status: {response.status_code}")
        print(response.text)

def send_news():
    print("📡 Fetching news...")
    general = fetch_general_news()
    tech = fetch_tech_news()
    sports = fetch_sports_news()
    ai = fetch_ai_news()

    message = format_news_message(general, tech, sports, ai)
    send_telegram_message(message)

if __name__ == "__main__":
    print("🤖 NewsBot started!")
    
    send_news()

    schedule.every().day.at("08:00").do(send_news)

    print("⏰ Scheduled to send daily at 8:00 AM. Bot is running...")

    while True:
        schedule.run_pending()
        time.sleep(60)