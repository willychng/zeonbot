import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

# Load bot token from .env file
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

# Set up intents
intents = discord.Intents.default()
intents.message_content = True  # Required for reading message content

# Set up the bot
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user} (ID: {bot.user.id})")

@bot.command()
async def ping(ctx):
    await ctx.send("🏓 Pong!")

if __name__ == "__main__":
    bot.run(TOKEN)