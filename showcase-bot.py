import os
import toml

import discord
from discord import Intents, Embed, Message, Attachment, File, ApplicationContext
from dotenv import load_dotenv

load_dotenv()
CONFIG = toml.load('config.toml')
MONITORED_CHANNEL_IDS = CONFIG.get('MONITORED_CHANNEL_IDS', [])
AUTOSTAR_CHANNELS = CONFIG.get('AUTOSTAR_CHANNELS', [])

intents = Intents.default() | Intents.message_content
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"Logged in as {client.user}!")

@client.event
async def on_message(message: Message):
    try:
        if message.channel.id in MONITORED_CHANNEL_IDS and message.attachments:
            if len(message.attachments) > 3:
                await message.reply("👋 The showcase channels have a limit of 3 images per post. Please do not upload more than three images. Please remove some image\(s\) from your post so that it has no more than 3 images.")
                return
                
        elif message.channel.id in AUTOSTAR_CHANNELS and message.attachments:
             await message.add_reaction("⭐")
    except Exception as e:
        print("Something went wrong.")
        pass

client.run(os.environ["BOT_TOKEN"])
