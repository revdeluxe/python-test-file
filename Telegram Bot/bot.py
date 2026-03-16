import os
import telebot
import requests
from dotenv import load_dotenv

# Import your existing provider logic
from providers.google_llm import GoogleProvider
from providers.local_llm import LocalProvider

load_dotenv()

# Configuration
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
USE_PROVIDER = "google" # Change to "local" if you want to use gemma-3

# Initialize AI Provider based on your switch
if USE_PROVIDER == "google":
    ai = GoogleProvider()
else:
    ai = LocalProvider()

# Initialize Telegram Bot
bot = telebot.TeleBot(TELEGRAM_TOKEN)

@bot.message_handler(commands=['start', 'help'])
def welcome(message):
    bot.reply_to(message, "👋 Welcome to TechHaven! I'm your AI clerk. How can I help you today?")

@bot.message_handler(commands=['catalog'])
def send_catalog(message):
    try:
        # Fetch products from Flask
        data = requests.get("http://127.0.0.1:5000/get_context").json()
        products = data.get('products', [])
        
        # Build a nice message
        msg = "🛍️ **Here is our current inventory:**\n\n"
        for p in products:
            status = "✅ In Stock" if p['stock'] > 0 else "❌ Out of Stock"
            msg += f"🔹 **{p['name']}** - {p['price']}\n   _{p['desc']}_\n   {status}\n\n"
            
        bot.reply_to(message, msg, parse_mode="Markdown")
    except requests.exceptions.ConnectionError:
        bot.reply_to(message, "Sorry, I can't reach the warehouse right now.")
@bot.message_handler(func=lambda m: True)
def handle_message(message):
    try:
        # 1. Get promo AND products from Flask
        try:
            data = requests.get("http://127.0.0.1:5000/get_context").json()
            promo = data.get('promo', '')
            products = data.get('products', [])
        except requests.exceptions.ConnectionError:
            promo = "No active promos."
            products = []
        
        # 2. Format the product list for the AI to read
        catalog_text = "\n".join([f"- {p['name']} ({p['price']}): {p['stock']} in stock. {p['desc']}" for p in products])
        
        # 3. Build the Ultimate System Prompt
        full_prompt = (
            f"System: You are Rev's Butler, a helpful AI store clerk. "
            f"Only recommend products from the following catalog. If an item is out of stock, apologize and offer an alternative.\n\n"
            f"--- CATALOG ---\n{catalog_text}\n\n"
            f"--- PROMO ---\n{promo}\n\n"
            f"User asks: {message.text}"
        )
        
        # 4. Generate response using your AIProvider
        ai_response = ai.generate(full_prompt)
        
        # 5. Log and Reply
        try:
            requests.post("http://127.0.0.1:5000/log_interaction", json={
                "user_id": str(message.from_user.id),
                "text": message.text,
                "response": ai_response
            })
        except requests.exceptions.ConnectionError:
            pass
            
        bot.reply_to(message, ai_response)

    except Exception as e:
        print(f"Error processing message: {e}")
        bot.reply_to(message, "Sorry, my systems are updating. Please try again in a moment!")
        
if __name__ == "__main__":
    print(f"Telegram Bot started! Brains: {USE_PROVIDER.upper()}")
    bot.infinity_polling()