import discord
import os
import requests
import logging
from logging.handlers import TimedRotatingFileHandler
import datetime
from dotenv import load_dotenv

# Custom exception
class clientException(Exception):
    pass;

FILE_PATH = 'log.txt'
logger = logging.getLogger('bot_log')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler = TimedRotatingFileHandler("bot.log",when='midnight',endcoding='utf-8')

logger.setLevel(logging.INFO)
handler.setFormatter(formatter)
logger.addHandler(handler) # Add handler(Handler obj which decides where logs go [Stream/File/TimedRotating]) to logger


# Loads the .env file
load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# intents = permissions for what events your bot can “see.”
Intents = discord.Intents.default() # Allows basic perms
Intents.message_content = True # enables on_message events (so your bot sees text messages).
client = discord.Client(intents = Intents) #creates the bot client, telling Discord “only send me the events I asked for.”

@client.event
async def on_ready():
    logger.error(f"We have logged in as {client.user}")


@client.event
async def on_message(message):
    # ignore message from ourselves
    if message.author == client.user:
        return 
    
    text = f"[{message.guild.name}] #{message.channel.name} | {message.author.name}: {message.content}"; # Craft the message
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage?chat_id={TELEGRAM_CHAT_ID}" # Pass telegram url into requests.get
    params = {"chat_id": TELEGRAM_CHAT_ID, "text": text}
    try:
        requests.get(url,params=params)
    except Exception as e:
        logger.error(f"Request.get failed. \n {e}")

try:
    client.run(DISCORD_TOKEN)
except Exception as e:
    logger.error(f"client.run{DISCORD_TOKEN} couldn't be ran. \n{e}")



