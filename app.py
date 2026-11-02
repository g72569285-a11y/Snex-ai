from flask import Flask, render_template, request, jsonify
import urllib.request
import urllib.parse
import json
import os

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
@app.route("/api/chat", methods=["POST"])
def chat():
    try:
        data = request.json
        user_message = data.get("message", "")

        if not user_message:
            return jsonify({"error": "Boş mesaj gönderilemez"}), 400

        # Pollinations AI Doğrudan Uç Noktası (Anahtarsız, Sınırsız, Çok Dilli)
        encoded_msg = urllib.parse.quote(user_message)
        url = f"https://text.pollinations.ai/{encoded_msg}?model=openai"
        
        req = urllib.request.Request(
            url, 
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        )

        with urllib.request.urlopen(req, timeout=15) as response:
            ai_reply = response.read().decode("utf-8")
            if not ai_reply or "<html>" in ai_reply:
                return jsonify({"error": "Model yanıt döndüremedi."}), 500
            return jsonify({"reply": ai_reply})

    except Exception as e:
        return jsonify({"error": f"Bağlantı hatası: {str(e)}"}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
