# Python Automation Bots

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=flat&logo=flask&logoColor=white)
![Groq](https://img.shields.io/badge/Groq_API-F55036?style=flat&logoColor=white)
![Model](https://img.shields.io/badge/LLaMA_3.3--70B-0467DF?style=flat&logoColor=white)
![Telegram](https://img.shields.io/badge/Telegram_API-26A5E4?style=flat&logo=telegram&logoColor=white)
![Status](https://img.shields.io/badge/Status-Live-brightgreen?style=flat)

Three real-world automation projects: a browser-based voice AI assistant, a daily news bot, and a price-tracking scraper. Each project came from an actual need. Each runs on its own after setup.

---

## Projects

### Icarus -- Voice Assistant

A voice assistant that runs in the browser. You press start, speak, press stop, and it responds out loud in a British neural voice. It remembers the conversation across turns.

**Pipeline:**
```
[Browser UI] -> POST /start -> Flask opens mic -> sounddevice records audio chunks
     |
POST /stop -> numpy concatenates chunks -> WAV file saved to temp
     |
Google Speech Recognition -> transcribed text
     |
Groq API (LLaMA 3.3-70B) + conversation_history -> AI reply
     |
edge-tts -> MP3 generated -> plays back -> temp file deleted
     |
JSON response sent back -> Browser UI updates with text
```

**What makes it interesting:**
- Full UI with an animated orb, wave visualizer, and live status display -- built from scratch in HTML/CSS/JS
- Neural British voice (Microsoft Edge TTS -- "en-US-AndrewNeural") -- sounds nothing like a robot
- Maintains full conversation history so it remembers context across turns
- Server uses Python threading so audio playback doesn't block the HTTP response

**Stack:** Python, Flask, Groq API, Edge TTS, Google Speech Recognition, sounddevice, NumPy, HTML/CSS/JS

---

### Telegram News Bot

Fetches top stories from four categories every morning and sends a formatted digest to Telegram automatically. No apps to open, no manual checking.

**Pipeline:**
```
schedule library -> triggers send_news() daily at 08:00
     |
4 fetch functions -> NewsAPI /top-headlines (general, tech, sports)
                  -> NewsAPI /everything (query: "AI OR LLM OR ChatGPT")
     |
format_news_message() -> Markdown digest with headlines + source + links
     |
Telegram Bot API /sendMessage -> delivered to chat
```

**Stack:** Python, NewsAPI, Telegram Bot API, schedule, python-dotenv

---

### Amazon Price Tracker

Monitors a product page every 6 hours. Saves every price to a JSON history file. Sends a Telegram alert the moment the price drops below your target -- with the exact drop amount and a direct buy link.

**Pipeline:**
```
schedule library -> triggers check_price() every 6 hours
     |
ScraperAPI -> proxies the Amazon request (bypasses bot detection)
     |
BeautifulSoup -> parses HTML -> finds price element
     |
price_history.json -> appends {price, timestamp} entry
     |
if current_price <= TARGET_PRICE:
    Telegram alert: price, drop amount, buy link
else:
    Telegram status: current vs target, highest/lowest seen
```

**Stack:** Python, BeautifulSoup, ScraperAPI, Telegram Bot API, schedule, python-dotenv

---

## How to Run

**1. Clone the repo**
```bash
git clone https://github.com/Navedh121/python-automation-bots.git
cd python-automation-bots
```

**2. Create a `.env` file in the project folder you want to run:**
```
GROQ_API_KEY=           # For Icarus -- get free at console.groq.com
TELEGRAM_BOT_TOKEN=     # Create a bot via @BotFather on Telegram
TELEGRAM_CHAT_ID=       # Your Telegram user/chat ID
NEWS_API_KEY=           # Free at newsapi.org
SCRAPER_API_KEY=        # Free tier at scraperapi.com
```

**3. Install and run:**
```bash
# Telegram News Bot
cd telegram-news-bot && pip install -r requirements.txt
python news_bot.py

# Amazon Price Tracker (edit PRODUCT_URL and TARGET_PRICE in the script first)
cd amazon-price-tracker && pip install -r requirements.txt
python price_tracker.py

# Icarus Voice Assistant
cd icarus-voice-assistant && pip install -r requirements.txt
python icarus.py
```

---

## Repo Structure

```
python-automation-bots/
├── icarus-voice-assistant/
│   ├── icarus.py           # Flask backend + speech pipeline
│   ├── icarus.html         # Animated browser UI
│   └── requirements.txt
├── telegram-news-bot/
│   ├── news_bot.py
│   └── requirements.txt
├── amazon-price-tracker/
│   ├── price_tracker.py
│   └── requirements.txt
└── .env                    # Not committed -- add your own keys
```

---

## Bugs I Hit (and Fixed)

- **PyAudio vs Python 3.14** -- PyAudio has no wheel for Python 3.14 on Windows. Switched to `sounddevice` + `scipy` for audio I/O instead.
- **Groq model deprecation** -- The model I originally used got decommissioned mid-build. Updated to `llama-3.3-70b-versatile`.
- **Amazon blocking the scraper** -- Direct requests to Amazon get blocked instantly. Routed everything through ScraperAPI to handle bot detection.

---

> Part of a learning series: [CLI tools](https://github.com/Navedh121/python-beginner-projects) -> [AI web apps](https://github.com/Navedh121/ai-web-apps) -> Automation bots
