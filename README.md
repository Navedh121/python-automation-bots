# Autonomous Python Agents

Three background agents I built from real personal needs. Each one runs on its own, talks to external APIs, and takes action without any manual input after setup.

Built by Navedh — second-year Electronics Engineering student from Kerala, India.

---

## Projects

### 1. Icarus — Voice Assistant

A voice assistant that runs in the browser. You press start, speak, press stop, and it responds out loud in a British neural voice. It remembers the conversation across turns.

**How it works:**

```
[Browser UI] → POST /start → Flask opens mic → sounddevice records audio chunks
     ↓
POST /stop → numpy concatenates chunks → WAV file saved to temp
     ↓
Google Speech Recognition → transcribed text
     ↓
Groq API (LLaMA 3.3 70b) + conversation_history → AI reply
     ↓
edge-tts → MP3 generated → playsound plays it → temp file deleted
     ↓
JSON response sent back → Browser UI updates with text
```

The server uses Python threading so audio playback doesn't block the HTTP response. Conversation history is kept in memory for the session, giving it context across multiple turns.

**Stack:** Python, Flask, Groq API (LLaMA 3.3), Google Speech Recognition, Microsoft Edge TTS, sounddevice, NumPy, HTML/CSS/JS

---

### 2. Telegram News Bot

Fetches top stories from four categories every morning and sends them to my Telegram automatically, formatted in clean Markdown. No apps to open, no manual checking.

**How it works:**

```
schedule library → triggers send_news() daily at 08:00
     ↓
4 parallel fetch functions → NewsAPI /top-headlines (general, tech, sports)
                           → NewsAPI /everything (query: "AI OR LLM OR ChatGPT")
     ↓
format_news_message() → builds a Markdown digest with headlines + source + read-more links
     ↓
Telegram Bot API /sendMessage → delivered to chat
     ↓
while True loop (60s sleep) → keeps scheduler alive
```

**Stack:** Python, NewsAPI, Telegram Bot API, schedule, requests, python-dotenv

---

### 3. Amazon Price Tracker

Monitors a product page every 6 hours. Saves every price it sees to a JSON history file. Sends a Telegram alert the moment the price drops below my target — with the exact drop amount and a buy link.

**How it works:**

```
schedule library → triggers check_price() every 6 hours
     ↓
ScraperAPI → proxies the Amazon request (bypasses bot detection)
     ↓
BeautifulSoup → parses HTML → finds price element (a-price-whole)
     ↓
price_history.json → appends {price, timestamp} entry
     ↓
if current_price ≤ TARGET_PRICE:
    send_alert() → Telegram: price, drop amount, buy link
else:
    send_status_update() → Telegram: current vs target, highest/lowest seen, checks done
```

**Stack:** Python, BeautifulSoup, ScraperAPI, Telegram Bot API, schedule, requests, python-dotenv

---

## Setup

Each project lives in its own folder and needs its own set of API keys.

**1. Clone the repo**
```bash
git clone https://github.com/Navedh121/python-automation-bots.git
cd python-automation-bots
```

**2. Create a `.env` file** in whichever project folder you want to run (copy from `.env.example`):
```
TELEGRAM_TOKEN=your-telegram-bot-token
CHAT_ID=your-telegram-chat-id
NEWS_API_KEY=your-newsapi-key          # for telegram-news-bot
SCRAPER_API_KEY=your-scraperapi-key    # for amazon-price-tracker
GROQ_API_KEY=your-groq-api-key         # for icarus-voice-assistant
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Run the project you want**
```bash
# Telegram News Bot
python telegram-news-bot/news_bot.py

# Amazon Price Tracker (edit PRODUCT_URL and TARGET_PRICE in the script first)
python amazon-price-tracker/price_tracker.py

# Icarus Voice Assistant (browser opens automatically)
python icarus-voice-assistant/icarus.py
```

---

## Notes on Bugs I Hit

These weren't tutorial projects, so they came with real problems:

- **PyAudio vs Python 3.14** — PyAudio has no wheel for Python 3.14 on Windows. Switched to `sounddevice` + `scipy` for audio I/O instead.
- **Groq model deprecation** — The model I originally used got decommissioned mid-build. Had to update to `llama-3.3-70b-versatile` and adjust the API call.
- **Amazon blocking the scraper** — Direct requests to Amazon get blocked instantly. Routed everything through ScraperAPI to handle the bot detection.

Getting through these made the projects actually work. Open to feedback or questions.
