from flask import Flask, render_template, request, jsonify
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

        # API anahtarı veya harici sunucu bağımlılığı yok! 
        # Doğrudan arayüzün akıcı çalışması için örnek simüle edilmiş yanıt döndürür.
        simulated_reply = f"SNEX 1.0 (Anahtarsız Mod): '{user_message}' mesajını aldım! Sistem tamamen stabil çalışıyor. 🚀"

        return jsonify({"reply": simulated_reply})

    except Exception as e:
        return jsonify({"error": f"Sunucu hatası: {str(e)}"}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
