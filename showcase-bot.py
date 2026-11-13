import os
import toml

import discord
from discord import Intents, Message, app_commands
from dotenv import load_dotenv

load_dotenv()
CONFIG = toml.load('config.toml')
# Optional: while testing, list guild IDs here for near-instant command sync
# (global command registration can take up to ~1 hour to propagate).
DEBUG_GUILDS = CONFIG.get('DEBUG_GUILDS', [])

intents = Intents.default()


class ShowcaseBot(discord.Client):
    def __init__(self):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        for guild_id in DEBUG_GUILDS:
            guild = discord.Object(id=guild_id)
            self.tree.copy_global_to(guild=guild)
            await self.tree.sync(guild=guild)
        await self.tree.sync()

    async def on_ready(self):
        print(f"Logged in as {self.user}!")


client = ShowcaseBot()


@client.tree.context_menu(name="Add free star ⭐")
async def add_free_star(interaction: discord.Interaction, message: Message):
    if message.author.id != interaction.user.id:
        await interaction.response.send_message(
            "You can only add a star to one of your own messages.", ephemeral=True
        )
        return

    if not any((a.content_type or "").startswith("image/") for a in message.attachments):
        await interaction.response.send_message(
            "That message has no image attachments to star.", ephemeral=True
        )
        return

    try:
        await message.add_reaction("⭐")
    except discord.HTTPException as e:
        print("Something went wrong with free star.", e)
        await interaction.response.send_message(
            "Couldn't add the star reaction. Try again later.", ephemeral=True
        )
        return

    await interaction.response.send_message("⭐ Star added!", ephemeral=True)


client.run(os.environ["BOT_TOKEN"])
