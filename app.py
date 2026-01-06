from flask import Flask, jsonify, request, render_template
import requests
import time

app = Flask(__name__)

FX_API_URL = "https://api.fxratesapi.com/latest"
CACHE_TTL = 300  # 5 minutos

cache = {
    "timestamp": 0,
    "rates": {}
}

def get_rates():
    now = time.time()
    if now - cache["timestamp"] > CACHE_TTL:
        response = requests.get(FX_API_URL, timeout=5)
        data = response.json()
        cache["rates"] = data["rates"]
        cache["rates"][data["base"]] = 1.0
        cache["timestamp"] = now
    return cache["rates"]

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/rates")
def rates():
    return jsonify(sorted(get_rates().keys()))

@app.route("/convert")
def convert():
    amount = float(request.args.get("amount", 0))
    from_currency = request.args.get("from")
    to_currency = request.args.get("to")

    rates = get_rates()

    if from_currency not in rates or to_currency not in rates:
        return jsonify({"error": "Invalid currency"}), 400

    base_amount = amount / rates[from_currency]
    result = base_amount * rates[to_currency]

    return jsonify({
        "from": from_currency,
        "to": to_currency,
        "amount": amount,
        "result": round(result, 2)
    })

@app.route("/health")
def health():
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)