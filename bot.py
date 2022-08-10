import os
import re
import requests
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
WEATHER_API = os.getenv('WEATHER_API')
if not BOT_TOKEN or not WEATHER_API:
    print("env variables missing")

filter = ['päivä', 'day', 'sää', 'keli', 'weather', 'ulkona', 'kylmä']


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")


async def day(update: Update, context: ContextTypes.DEFAULT_TYPE):
    weather = requests.get(
        f"https://api.openweathermap.org/data/2.5/weather?q=otaniemi&appid={WEATHER_API}&lang=fi")
    weather = weather.json()
    await update.effective_chat.send_message(weather['weather'][0]['description'])
if __name__ == '__main__':
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)
    day_handler = CommandHandler('paiva', day)
    application.add_handler(day_handler)
    message_handler = MessageHandler(filters=(
        filters.CHAT & filters.Regex(re.compile('|'.join(filter)))), callback=day)
    application.add_handler(message_handler)
    application.run_polling()
