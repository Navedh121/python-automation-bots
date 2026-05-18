# Phase 3 — Automation & AI Agents

I'm Naved, a second year Electronics Engineering student from Kerala, India. This repository contains three projects I built while learning Python automation and AI development. Each one solves a real problem and taught me something new.

---

## What's in here

### 🤖 Telegram News Bot
I got tired of opening five different apps to catch up on the news. So I built a bot that does it for me — every morning it pulls the top stories across four categories and drops them straight into my Telegram.

Covers world news, tech, sports, and AI. Runs on a schedule automatically, no manual trigger needed.

**Built with:** Python, NewsAPI, Telegram Bot API, schedule

---

### 💰 Amazon Price Tracker
I wanted to buy something on Amazon but the price kept fluctuating. Instead of checking it every day manually, I wrote a script that checks it for me every few hours and sends me a Telegram alert the moment it drops below my target price. It also keeps a local history of every price it has seen.

**Built with:** Python, BeautifulSoup, ScraperAPI, Telegram Bot API

---

### 🎙️ Icarus — Voice Assistant
This one is my favourite. I built a voice assistant that runs in the browser — you press a button, speak, and it speaks back. It has a full UI with an animated orb, wave visualizer, and a chat log. The voice is a British neural voice that sounds close to Jarvis from Iron Man, which is exactly what I was going for.

Under the hood it uses Groq for the AI brain (free and fast), Edge TTS for the voice, and Google Speech Recognition to understand what I say. The whole thing runs locally on a Flask server.

**Built with:** Python, Flask, Groq AI (LLaMA 3.3), Edge TTS, Google Speech Recognition, HTML/CSS/JS

---

## How to run any of these

Each project has its own folder. You will need a `.env` file with your own API keys — check the individual files to see which keys are needed. They are not included here for obvious reasons.

```bash
pip install -r requirements.txt  # install dependencies
python news_bot.py               # or price_tracker.py or icarus.py
```

---

## A note

These are not perfect projects. There were bugs, library conflicts, and a lot of debugging along the way. But they all work, and building them taught me more than any tutorial could.

If you have any questions or want to collaborate, feel free to reach out.