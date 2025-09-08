import discord
import os
from dotenv import load_dotenv

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
    print(f"We have logged in as {client.user}")


@client.event
async def on_message(message):
    # ignore message from ourselves
    if message.author == client.user:
        return 
    
    await message.channel.send(f"[{message.guild.name}] #{message.channel.name} | {message.author.name}: {message.content}");

client.run(DISCORD_TOKEN)