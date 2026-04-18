# SachAI Telegram Bot

A production-quality Telegram bot designed to instantly fact-check suspicious forwards, news articles, and links. It connects directly to your existing SachAI FastAPI backend.

## Features
- **Zero-Friction UX:** Just paste or forward a message. No commands needed!
- **AI Analysis:** Displays Verdict, Fake News Risk, and Credibility Score.
- **Societal Impact Warnings:** Explains the potential real-world harm of the claim.
- **Persuasive Tone:** Mildly Hinglish, friendly, yet authoritative when discouraging fake news spread.
- **Modular & Async:** Built with `python-telegram-bot` and `httpx`.

---

## Prerequisites
1. **Python 3.11+**
2. **SachAI Backend:** Your FastAPI backend must be running locally (usually on `http://127.0.0.1:8000`).

## Setup Instructions

### 1. Create the Bot on Telegram
1. Open Telegram and search for **@BotFather**.
2. Send the command `/newbot`.
3. Follow the prompts to choose a name (e.g., `SachAI`) and a username (e.g., `SachAIFactCheckBot`).
4. BotFather will give you a **HTTP API Token** (it looks like `123456789:ABCDefghIJKlmnop...`). Copy this.

### 2. Configure Environment Variables
1. Rename `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```
2. Open `.env` and paste your BotFather token into the `TELEGRAM_BOT_TOKEN` variable.
   *(Make sure `SACH_AI_BACKEND_URL` correctly points to your running FastAPI server)*.

### 3. Install Dependencies
Open your terminal in the `sachai-telegram-bot` directory and run:
```bash
pip install -r requirements.txt
```

### 4. Run the Bot
Ensure your FastAPI backend is running in one terminal. In a new terminal, start the bot:
```bash
python telegram_bot.py
```
You should see logs indicating the bot is initializing and polling for updates!

---

## Testing
1. Go to Telegram and search for the bot username you created.
2. Click **Start** (or type `/start`). It will introduce itself.
3. **Copy & Paste** any suspicious text or forward a message to it.
4. The bot will show a "typing..." action, query your SachAI backend, and return a beautifully formatted Markdown analysis.
