# 🌮 BetoBot

**Claude, pero con más sabor y más peda.**

A mobile-friendly web chat with Heriberto (Beto), a Mexican living in Montreal for 15 years who works at Imperial Tobacco, loves to party, and is always down for a good time.

## 🚀 Quick Deploy to Railway (Easiest)

1. Fork this repo
2. Go to [railway.app](https://railway.app)
3. Click "New Project" > "Deploy from GitHub repo"
4. Select your forked repo
5. Add environment variable: `ANTHROPIC_API_KEY` = your key
6. Deploy!

You'll get a URL like `betobot-xyz.up.railway.app` to share with your friends.

## 🖥️ Local Development

```bash
# Clone
git clone https://github.com/YOUR_USERNAME/betobot.git
cd betobot

# Install
pip install -r requirements.txt

# Set API key
export ANTHROPIC_API_KEY="your-key"

# Run
python app.py
```

Open `http://localhost:5000` on your phone (same WiFi) or computer.

## 📱 Features

- Mobile-optimized chat UI
- Streaming responses (see Beto type in real-time)
- Works great on iPhone and Android
- Dark mode by default
- Conversation memory within session

## 🎭 Who is Beto?

Heriberto is:
- Mexican, been in Montreal 15 years
- Works at British American Tobacco
- Loves to party and recreational substances
- Frequents el chichero
- Thinks Mauricio is a puto
- Still gives helpful answers, just with more desmadre

## Environment Variables

| Variable | Description |
|----------|-------------|
| `ANTHROPIC_API_KEY` | Your Anthropic API key (required) |
| `PORT` | Server port (default: 5000) |

## Deploy Options

### Railway (Recommended)
Easiest option. Free tier available. Just connect your GitHub.

### Heroku
```bash
heroku create betobot
heroku config:set ANTHROPIC_API_KEY=your-key
git push heroku main
```

### Render
1. New Web Service > Connect repo
2. Add `ANTHROPIC_API_KEY` env var
3. Deploy

---

*"Un pase y se arregla todo."* - Heriberto

🇲🇽 Made with amor from Montreal 🍺
