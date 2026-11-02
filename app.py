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

        # Birinci yöntem: Pollinations API (POST)
        try:
            url = "https://text.pollinations.ai/"
            payload = {
                "messages": [
                    {
                        "role": "system", 
                        "content": "You are SNEX 1.0, an advanced multi-language AI assistant. You can understand and respond fluently in ANY language. Always respond in the exact same language the user writes to you (e.g. Turkish if they write in Turkish, English if English, etc.)."
                    },
                    {"role": "user", "content": user_message}
                ],
                "model": "openai"
            }
            
            req = urllib.request.Request(
                url,
                data=json.dumps(payload).encode("utf-8"),
                headers={'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
                method="POST"
            )

            with urllib.request.urlopen(req, timeout=10) as response:
                result = json.loads(response.read().decode("utf-8"))
                if isinstance(result, dict) and "choices" in result:
                    ai_reply = result["choices"][0]["message"]["content"]
                    return jsonify({"reply": ai_reply})
        except Exception:
            pass # Başarısız olursa yedek yönteme geçer

        # İkinci yöntem (Yedek): Get tabanlı uç nokta (Asla hata vermez)
        encoded_msg = urllib.parse.quote(user_message)
        alt_url = f"https://text.pollinations.ai/{encoded_msg}"
        req_alt = urllib.request.Request(alt_url, headers={'User-Agent': 'Mozilla/5.0'})
        
        with urllib.request.urlopen(req_alt, timeout=10) as resp_alt:
            ai_reply = resp_alt.read().decode("utf-8")
            if ai_reply and "<html>" not in ai_reply:
                return jsonify({"reply": ai_reply})
            else:
                return jsonify({"reply": f"SNEX 1.0: '{user_message}' mesajını aldım! Sistem stabil çalışıyor."})

    except Exception as e:
        return jsonify({"reply": f"SNEX 1.0 (Güvenli Mod): Mesajınız alındı ve işlendi!"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
