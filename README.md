# Phase 3 — Automation and AI Agents

Second year Electronics Engineering student from Kerala, India. This repo has three projects I built while learning Python automation. Each project came from a real need, not just a tutorial exercise.

---

## Projects

### Telegram News Bot

I was spending too much time jumping between apps to read the news. Built a bot that pulls top stories every morning and sends them to my Telegram automatically, sorted into four sections: world news, tech, sports, and AI. Set it and forget it.

Stack: Python, NewsAPI, Telegram Bot API, schedule library

---

### Amazon Price Tracker

Wanted to buy a perfume but the price kept changing. Instead of checking manually every day, I wrote a script that monitors the price every few hours and sends me a Telegram alert when it falls below a number I set. It also saves a history of every price it has checked.

Stack: Python, BeautifulSoup, ScraperAPI, Telegram Bot API

---

### Icarus Voice Assistant

My favourite one. A voice assistant that runs in the browser with a full UI. You press start, say something, press stop, and it responds out loud in a British neural voice. There is an animated orb and wave visualizer that reacts when speaking. Named it Icarus.

The backend is a Flask server. Speech recognition is handled by Google, the AI brain runs on Groq (LLaMA 3.3), and the voice is generated using Microsoft Edge TTS.

Stack: Python, Flask, Groq API, Edge TTS, Google Speech Recognition, HTML, CSS, JavaScript

---

## Setup

Each project sits in its own folder. You will need a `.env` file with your own API keys to run any of them. The keys are not included here.

Install dependencies for whichever project you want to run:

```bash
pip install -r requirements.txt
python news_bot.py
```

---

## Notes

There were bugs. PyAudio would not install on Python 3.14, a Groq model got decommissioned mid-build, Amazon blocked the scraper. Got through all of it. The projects work.

Open to feedback or questions.
