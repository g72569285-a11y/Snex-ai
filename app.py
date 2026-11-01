from flask import Flask, render_template, request, jsonify
import urllib.request
import json
import os

app = Flask(__name__)

# --- API ANAHTARIN BURADA GİZLİ KALIYOR ---
GEMINI_API_KEY = "AQ.Ab8RN6JKlEQwHuT6G1qspEreqj5wZrbtoTRNm1xl1VJhNbtbTA"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.json
        user_message = data.get("message", "")
        model = data.get("model", "gemini-1.5-flash")

        if not user_message:
            return jsonify({"error": "Boş mesaj gönderilemez"}), 400

        # Google Gemini API Çağrısı
        url = f"https://generativelanguage.googleapis.com/v1/models/{model}:generateContent?key={GEMINI_API_KEY}"
        payload = {"contents": [{"parts": [{"text": user_message}]}]}
        headers = {'Content-Type': 'application/json'}

        req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers=headers)
        
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode("utf-8"))
            reply = result["candidates"][0]["content"]["parts"][0]["text"]
            return jsonify({"reply": reply})

    except Exception as e:
        return jsonify({"error": f"Sunucu hatası: {str(e)}"}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)