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
logger = logging.getLogger()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler = TimedRotatingFileHandler("bot.log",when='midnight',encoding='utf-8')

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

def forward_attachments(attachment):
    if attachment.content_type.startswith("image/"):
        #Call telegram sendPhoto
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto"
        params = {"chat_id": TELEGRAM_CHAT_ID, "photo": attachment.url}
        try:
            requests.post(url,params=params)
        except Exception as e:
            logger.error(f"sendPhoto failed. \n {e}")
    else:
        #Call telegram sendDocument
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendDocument"
        params = {"chat_id": TELEGRAM_CHAT_ID, "document": attachment.url}
        try:
            requests.post(url,params=params)
        except Exception as e:
            logger.error(f"sendDocument failed. \n {e}")

@client.event
async def on_ready():
    logger.info(f"We have logged in as {client.user}")

@client.event
async def on_message(message):
    # ignore message from ourselves
    if message.author == client.user:
        return 
    if message.content:
        text = f"[{message.guild.name}] #{message.channel.name} | {message.author.name}: {message.content}"; # Craft the message
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage?chat_id={TELEGRAM_CHAT_ID}" # Pass telegram url into requests.get
        params = {"chat_id": TELEGRAM_CHAT_ID, "text": text}
        try:
            requests.post(url,params=params)
        except Exception as e:
            logger.error(f"sendMessage failed. \n {e}")

    for attachment in message.attachments:
        forward_attachments(attachment)



try:
    client.run(DISCORD_TOKEN)
except Exception as e:
    logger.error(f"client.run{DISCORD_TOKEN} couldn't be ran. \n{e}")



