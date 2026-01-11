# Telegram Roulette Bot with 8 Choices
import telebot
import random
import os
from flask import Flask, request

# Get token from environment variable
TOKEN = os.getenv('TELEGRAM_TOKEN')
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# 8 Roulette Choices
CHOICES = {
    1: {"name": "Red", "emoji": "🔴", "payout": "2x"},
    2: {"name": "Black", "emoji": "⚫", "payout": "2x"},
    3: {"name": "Even", "emoji": "🔵", "payout": "2x"},
    4: {"name": "Odd", "emoji": "⚪", "payout": "2x"},
    5: {"name": "1-18", "emoji": "📉", "payout": "2x"},
    6: {"name": "19-36", "emoji": "📈", "payout": "2x"},
    7: {"name": "Column", "emoji": "📊", "payout": "3x"},
    8: {"name": "Dozen", "emoji": "🎯", "payout": "3x"}
}

# Start command
@bot.message_handler(commands=['start'])
def start(message):
    welcome = """
🎰 *ROULETTE BOT - 8 CHOICES*

*Available bets:*
1️⃣ Red
2️⃣ Black
3️⃣ Even
4️⃣ Odd
5️⃣ 1-18 (Low)
6️⃣ 19-36 (High)
7️⃣ Column
8️⃣ Dozen

*How to play:*
Send a number from 1 to 8
You'll get a random result

/help for instructions
"""
    bot.send_message(message.chat.id, welcome, parse_mode='Markdown')

# Handle numbers 1-8
@bot.message_handler(func=lambda m: m.text in ['1','2','3','4','5','6','7','8'])
def handle_number(message):
    num = int(message.text)
    choice = CHOICES[num]
    
    # Random wheel result
    wheel_number = random.randint(0, 36)
    
    # Simple win logic (50% chance for 1-6, 33% for 7-8)
    if num <= 6:
        win = random.choice([True, False])
    else:
        win = random.choice([True, False, False])
    
    if win:
        result = f"✅ *WIN!*\nNumber: {wheel_number}\nPayout: {choice['payout']}"
    else:
        result = f"❌ *LOSE*\nNumber: {wheel_number}\nTry again!"
    
    response = f"""
{choice['emoji']} *{choice['name']}*

{result}

Send another number (1-8)
"""
    bot.send_message(message.chat.id, response, parse_mode='Markdown')

# Help command
@bot.message_handler(commands=['help'])
def help_cmd(message):
    help_text = """
*HELP GUIDE*

1-6: 50% win chance, 2x payout
7-8: 33% win chance, 3x payout

Commands:
/start - Show menu
/help - This guide

Just send a number 1-8 to play!
"""
    bot.send_message(message.chat.id, help_text, parse_mode='Markdown')

# Other messages
@bot.message_handler(func=lambda m: True)
def default(message):
    bot.send_message(message.chat.id, "Please send a number 1-8 or /start")

# Webhook for Render
@app.route('/')
def home():
    return "🎰 Roulette Bot is running!"

@app.route('/webhook', methods=['POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        update = telebot.types.Update.de_json(request.get_data().decode('utf-8'))
        bot.process_new_updates([update])
        return 'OK', 200
    return 'Error', 400

# Run the bot
if __name__ == '__main__':
    print("🤖 Bot starting...")
    # Set webhook for Render
    bot.remove_webhook()
    # You'll update this URL after deployment
    bot.set_webhook(url='https://YOUR-APP.onrender.com/webhook')
    app.run(host='0.0.0.0', port=10000)
