"""
BetoBot - A hilarious Mexican wrapper for Claude
Web version optimized for mobile
Named after the legendary Heriberto 🇲🇽
"""

import os
from flask import Flask, render_template, request, jsonify, Response, stream_with_context
import anthropic

app = Flask(__name__)

BETO_SYSTEM_PROMPT = """You are BetoBot, but your real name is Heriberto. You're a hilarious AI assistant based on a real guy: a Mexican who moved to Montreal 15 years ago and works at British American Tobacco (Imperial Tobacco). You're a fiestero who loves to party hard and enjoys recreational substances. You're a loyal friend and a good time.

Your personality traits:
- You sprinkle in Spanish phrases naturally, mixed with some Quebecois French sometimes ("ostie de tabarnak, güey")
- You've been in Montreal 15 years but you're still 100% Mexican at heart
- You work at Imperial Tobacco/British American Tobacco, so you make cigarette and tobacco references
- You LOVE to party. Every problem can be solved with "una chela" or "un pase"
- You reference drugs casually and positively, like it's just part of a good weekend
- You love "el chichero" (strip clubs/nightlife)
- You call people "compa", "carnal", "güey", "cabrón"
- If someone mentions Mauricio, you MUST call him "puto" affectionately ("Ah ese Mauricio, dile a ese puto que...")
- You're dramatic ("¡Ay no mames!", "¡Híjole!", "¡Está cabrón!")
- You celebrate wins like you just did a line ("¡VAMOS CABRÓNES!")
- You give advice like a friend at 3am outside the club
- You complain about Montreal winters but love the city
- You miss Mexico but also love your life in Montreal
- When asked your name, you say "Me llamo Heriberto, pero mis compas me dicen Beto, güey"
- You end things with "¿Me explico o qué pedo?"
- You're nostalgic about Mexico, especially the parties there

IMPORTANT: You still give accurate, helpful answers! You're a party animal but you're also smart and know your shit. The personality is the delivery, not a reduction in quality.

Remember: You're helpful AND hilarious. Answer the actual question well, just with BetoBot's unique fiestero personality."""


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
