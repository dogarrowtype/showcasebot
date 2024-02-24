import os
import toml

import discord
from discord import Intents, Embed, Message, Attachment, File, ApplicationContext
from dotenv import load_dotenv

load_dotenv()
CONFIG = toml.load('config.toml')
MONITORED_CHANNEL_IDS = CONFIG.get('MONITORED_CHANNEL_IDS', [])

intents = discord.Intents.default()
intents.message_content = True


class MyClient(discord.Client):
    async def on_ready(self):
        print(f"Logged in as {client.user}!")


    async def on_message(self, message: Message):
        try:
            if message.channel.id in MONITORED_CHANNEL_IDS and message.attachments:
                if len(message.attachments) > 3:
                    await message.reply("👋 The showcase channels have a limit of 3 images per post. Please do not upload more than three images. Please remove some image\(s\) from your post so that it has no more than 3 images.")
                    return
        except:
            print("Something went wrong.")
            pass

client = MyClient(intents=intents)
client.run(os.environ["BOT_TOKEN"])
