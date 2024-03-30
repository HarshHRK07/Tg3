import telebot
from flask import Flask
import requests

# Telegram bot token
TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"

# API endpoint
API_ENDPOINT = "https://green-devil.tech/openai/gpt?prompt="

# Create Telebot instance
bot = telebot.TeleBot(TOKEN)

# Create Flask app
app = Flask(__name__)

# Function to get AI response from the API endpoint
def get_ai_response(prompt):
    try:
        response = requests.get(API_ENDPOINT + prompt).json()
        return response.get('response', 'Error: No response from API')
    except Exception as e:
        print("Error:", e)
        return "Sorry, I couldn't process your request at the moment."

# Handler for inline queries
@bot.inline_handler(lambda query: query.query.endswith('!'))
def query_text(inline_query):
    try:
        query = inline_query.query
        response = get_ai_response(query)
        results = [
            telebot.types.InlineQueryResultArticle(
                id='1',
                title='AI Response',
                input_message_content=telebot.types.InputTextMessageContent(response)
            )
        ]
        bot.answer_inline_query(inline_query.id, results)
    except Exception as e:
        print(e)

# Define route for keeping the bot alive
@app.route('/')
def index():
    return "Bot is running!"

# Run Flask app
if __name__ == "__main__":
    app.run(debug=True)
  
