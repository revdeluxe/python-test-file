from flask import Flask, render_template, request, redirect
from datetime import datetime

app = Flask(__name__)

# Global state (In production, use a Database like SQLite)
store_data = {
    "current_promo": "Free shipping on orders over $50!",
    "logs": [],
    "products": [
        {"name": "Neon Mechanical Keyboard", "price": "$89", "stock": 15, "desc": "Clicky switches with RGB lighting."},
        {"name": "Quantum Coffee Mug", "price": "$25", "stock": 0, "desc": "Keeps coffee hot forever. Currently out of stock!"},
        {"name": "Holographic Monitor", "price": "$450", "stock": 5, "desc": "3D display without glasses."}
    ]
}

@app.route('/')
def index():
    return render_template('dashboard.html', 
                           logs=reversed(store_data["logs"]), 
                           total_queries=len(store_data["logs"]))

@app.route('/get_context', methods=['GET'])
def get_context():
    # Now it returns BOTH the promo and the product list
    return {
        "promo": store_data["current_promo"],
        "products": store_data["products"]
    }

@app.route('/log_interaction', methods=['POST'])
def log_interaction():
    data = request.json
    new_entry = {
        "user": data.get("user_id"),
        "text": data.get("text"),
        "response": data.get("response"),
        "time": datetime.now().strftime("%H:%M:%S")
    }
    store_data["logs"].append(new_entry)
    return {"status": "success"}

        # ...existing code...

@app.route('/update_promo', methods=['POST'])
def update_promo():
    store_data["current_promo"] = request.form.get("promo")
    return redirect('/')

if __name__ == "__main__":
    app.run(port=5000, debug=True)