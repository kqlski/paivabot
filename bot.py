import os
from random import random
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

filter = ['päivä', 'day', 'sää', 'keli', 'weather', 'ulkona',
          'kylmä', 'lämmin', 'sataa', 'sade', 'lunta', 'lumi']


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")


async def day(update: Update, context: ContextTypes.DEFAULT_TYPE):
    weather = requests.get(
        f"https://api.openweathermap.org/data/2.5/weather?q=otaniemi&appid={WEATHER_API}&units=metric&lang=fi")
    weather = weather.json()
    descriptives = weather['weather'][0]
    weather_desc = descriptives['description']
    code = descriptives['id']
    measurements = weather['main']
    temp = measurements['temp']
    moist = measurements['humidity']
    beautiful_pct=0

    #https://openweathermap.org/weather-conditions
    match code//100:
        case 8: #clouds
            match code%100:
                case 0:
                    beautiful_pct=100# clear sky
                case 1:
                    beautiful_pct=75+random()*11  # 11-25% cloudy
                case 2:
                    beautiful_pct=50+random()*25#25-50% cloudy
                case 3:
                    beautiful_pct=16+random()*33#51-84% broken
                case 4:
                    beautiful_pct=random()*15
            pass
        case 6:#snow
            
            pass
        case 5:#rain
            pass
        case 3:#drizzle
            pass


        
    await update.effective_chat.send_message(f"{weather_desc}: {temp:.1f} °C, {moist} % 💦\nPäivä: ")
if __name__ == '__main__':
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)
    day_handler = CommandHandler('paiva', day)
    application.add_handler(day_handler)
    message_handler = MessageHandler(filters=(
        filters.CHAT & filters.Regex(re.compile('|'.join(filter), re.IGNORECASE))), callback=day)
    application.add_handler(message_handler)
    application.run_polling()
