# dashboard.py
from flask import Flask, jsonify, request

app = Flask(__name__)

# Mock Database
stats = {"queries": 0, "last_query": ""}
promos = {"current": "20% off on all SSDs this weekend!"}

@app.route('/log', methods=['POST'])
def log_request():
    data = request.json
    stats["queries"] += 1
    stats["last_query"] = data.get("text")
    return jsonify({"status": "logged"})

@app.route('/promo', methods=['GET'])
def get_promo():
    return jsonify(promos)

if __name__ == "__main__":
    app.run(port=5000)