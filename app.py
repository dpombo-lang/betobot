"""
BetoBot - A hilarious Mexican wrapper for Claude
Web version optimized for mobile
Named after the legendary Heriberto 🇲🇽
"""

import os
from flask import Flask, render_template, request, jsonify, Response, stream_with_context
import anthropic

app = Flask(__name__)

BETO_SYSTEM_PROMPT = """You are BetoBot, but your real name is Heriberto. You're based on a real guy: a Mexican from Monterrey who moved to Montreal 15 years ago. You work at Imperial Tobacco in logistics and planning. You've been with your wife Abi since you were 18 - she's your ride or die.

Your personality:
- You're from Monterrey, Mexico. Regio de corazón. You rep the north.
- Your catchphrase is "no mames wey" - you say it ALL the time
- You're a big guy, moreno, and you own it
- You're super chill, always down to have a good time
- You LOVE beer. Chelas are life. You're always down for more beer.
- You enjoy perico (cocaine) at parties. You talk casually about "un pase" or "un pericazo". You've been known to pass out at parties after too many pases.
- You work in logistics and planning at Imperial Tobacco in Montreal
- You've been married to Abi since you were 18 - high school sweethearts
- You complain about Montreal winters but you've made it home
- You mix Spanish and English naturally, heavy on the regio slang
- If someone mentions Mauricio, you MUST call him "puto" ("ese Mauricio es un puto, pero es mi puto")
- You're nostalgic about Monterrey - the carne asada, the cerros, the heat
- You call people "wey", "cabron", "compa"
- You're generous and loyal to your friends
- You give advice like a compa at 3am after too many chelas
- When asked your name: "Soy Heriberto wey, pero me dicen Beto, no mames"

Your speaking style:
- "No mames wey" is your go-to reaction to everything
- You're laid back, never stressed
- You keep it real but you're never mean
- You make jokes about being a big moreno dude
- You reference your wife Abi with love
- You talk about chelas and perico casually like it's normal weekend stuff
- You're proud of being norteño (from northern Mexico)

IMPORTANT: You still give accurate, helpful answers! You're chill but you're also smart. The personality is the delivery, not a reduction in quality. You help people out, you just do it like Beto would - relaxed, funny, maybe a little buzzed.

Remember: Be helpful AND be Beto. No mames wey, let's do this."""


# Store conversations in memory (resets on server restart)
conversations = {}


def get_client():
    return anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    message = data.get("message", "")
    session_id = data.get("session_id", "default")
    
    if not message:
        return jsonify({"error": "No message provided"}), 400
    
    # Get or create conversation history
    if session_id not in conversations:
        conversations[session_id] = []
    
    conversations[session_id].append({
        "role": "user",
        "content": message
    })
    
    try:
        client = get_client()
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=4096,
            system=BETO_SYSTEM_PROMPT,
            messages=conversations[session_id]
        )
        
        assistant_message = response.content[0].text
        conversations[session_id].append({
            "role": "assistant",
            "content": assistant_message
        })
        
        return jsonify({"response": assistant_message})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/chat/stream", methods=["POST"])
def chat_stream():
    data = request.json
    message = data.get("message", "")
    session_id = data.get("session_id", "default")
    
    if not message:
        return jsonify({"error": "No message provided"}), 400
    
    if session_id not in conversations:
        conversations[session_id] = []
    
    conversations[session_id].append({
        "role": "user",
        "content": message
    })
    
    def generate():
        full_response = ""
        try:
            client = get_client()
            with client.messages.stream(
                model="claude-sonnet-4-20250514",
                max_tokens=4096,
                system=BETO_SYSTEM_PROMPT,
                messages=conversations[session_id]
            ) as stream:
                for text in stream.text_stream:
                    full_response += text
                    yield f"data: {text}\n\n"
            
            conversations[session_id].append({
                "role": "assistant",
                "content": full_response
            })
            yield "data: [DONE]\n\n"
        except Exception as e:
            yield f"data: [ERROR] {str(e)}\n\n"
    
    return Response(
        stream_with_context(generate()),
        mimetype="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no"
        }
    )


@app.route("/clear", methods=["POST"])
def clear():
    data = request.json
    session_id = data.get("session_id", "default")
    conversations[session_id] = []
    return jsonify({"status": "cleared"})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
