# Python Automation Bots

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=flat&logo=flask&logoColor=white)
![Groq](https://img.shields.io/badge/Groq_API-F55036?style=flat&logoColor=white)
![Model](https://img.shields.io/badge/LLaMA_3.3--70B-0467DF?style=flat&logoColor=white)
![Telegram](https://img.shields.io/badge/Telegram_API-26A5E4?style=flat&logo=telegram&logoColor=white)
![Status](https://img.shields.io/badge/Status-Live-brightgreen?style=flat)

Three real-world automation projects: a browser-based voice AI assistant, a daily news bot, and a price-tracking scraper. Built by a 2nd-year Electronics Engineering student from Kerala. Each project came from an actual need.

---

## Projects

### Icarus — Voice Assistant

A browser-based voice AI that runs a full conversation loop: you speak, it listens, thinks, and talks back.

**Pipeline:**
```
Microphone → sounddevice (record) → Google Speech Recognition (STT)
→ Groq API / LLaMA 3.3-70B (think) → Microsoft Edge TTS (speak)
→ Flask (serve) → Browser UI (display)
```

**What makes it interesting:**
- Full UI with an animated orb, wave visualizer, and live status display — built from scratch in HTML/CSS/JS
- Neural British voice (Microsoft Edge TTS — "en-US-AndrewNeural") — sounds nothing like a robot
- Maintains full conversation history so it remembers context across turns
- Named Icarus; has a personality ("a brilliant AI inspired by Jarvis from Iron Man")
- Handled a real obstacle: PyAudio wouldn't install on Python 3.14 → switched to `sounddevice` + `scipy`

**Stack:** Python, Flask, Groq API, Edge TTS, Google Speech Recognition, sounddevice, HTML, CSS, JavaScript

---

### Telegram News Bot

Sends a formatted daily news digest to Telegram every morning at 8:00 AM. Four sections: world news, tech, sports, and AI/LLM news — all pulled fresh from NewsAPI and formatted with markdown and emojis.

Set it up once, forget about it, get the news delivered.

**Stack:** Python, NewsAPI, Telegram Bot API, `schedule` library

---

### Amazon Price Tracker

Monitors an Amazon product's price every 6 hours. Sends a Telegram alert when the price drops below a target you set. Also saves a full price history to a JSON file so you can see the price over time.

**The real challenge:** Amazon actively blocks scrapers. Solved it by routing requests through ScraperAPI, which handles proxy rotation and browser fingerprinting automatically.

**Stack:** Python, BeautifulSoup, ScraperAPI, Telegram Bot API, `schedule` library

---

## How to Run

Each project lives in its own folder with a `requirements.txt`.

```bash
# Example: run the Telegram news bot
cd telegram-news-bot
pip install -r requirements.txt

# Add your API keys to ../.env (see .env.example)
python news_bot.py
```

**Required API keys (add to `.env`):**
```
GROQ_API_KEY=          # For Icarus — get free at console.groq.com
TELEGRAM_BOT_TOKEN=    # Create a bot via @BotFather on Telegram
TELEGRAM_CHAT_ID=      # Your Telegram user/chat ID
NEWS_API_KEY=          # Free at newsapi.org
SCRAPER_API_KEY=       # Free tier at scraperapi.com
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
└── .env                    # Not committed — add your own keys
```

---

## Notes

There were bugs. PyAudio wouldn't install on Python 3.14. A Groq model got decommissioned mid-build. Amazon blocked the scraper. Got through all of it. The projects work.

---

> Part of a learning series: [CLI tools](https://github.com/Navedh121/python-projects) → [AI web apps](https://github.com/Navedh121/ai-projects) → Automation bots
