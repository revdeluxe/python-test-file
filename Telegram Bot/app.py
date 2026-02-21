import os
import telebot
from dotenv import load_dotenv
# Import your existing provider classes
from providers.google_llm import GoogleProvider
from providers.local_llm import LocalProvider

load_dotenv()

# --- CONFIGURATION ---
USE_PROVIDER = "google" # or "local"
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Initialize your AI Provider exactly like your screenshot
if USE_PROVIDER == "google":
    ai = GoogleProvider()
else:
    ai = LocalProvider(model_path="./models/gemma-3")

# Initialize the Telegram Bot
bot = telebot.TeleBot(TELEGRAM_TOKEN)

# --- BOT HANDLERS ---

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.reply_to(message, "Hello! I am your AI Product Clerk. How can I help you with our catalog today?")

@bot.message_handler(func=lambda message: True)
def handle_queries(message):
    """
    This replaces your Flask route. 
    It takes the TG message, sends it to your AI provider, and replies.
    """
    user_input = message.text
    
    try:
        # Assuming your provider has a method like .generate() or .query()
        # Adjust the method name below to match your 'base.py' interface
        ai_response = ai.query(user_input) 
        
        bot.reply_to(message, ai_response)
    except Exception as e:
        print(f"Error: {e}")
        bot.reply_to(message, "I encountered an error processing that request.")

# Start the bot (Replaces app.run())
if __name__ == "__main__":
    print(f"Bot is running using {USE_PROVIDER} provider...")
    bot.infinity_polling()