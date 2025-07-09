import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

import time

# Load bot token from .env file
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
STATUS_CHANNEL_ID = int(os.getenv("BOT_STATUS_CHANNEL_ID"))
LOG_CHANNEL_ID = int(os.getenv("BOT_LOG_CHANNEL_ID"))

ADMIN_ID = list(map(int, os.getenv("ADMIN_ID").split(',')))

# Set up intents
intents = discord.Intents.default()
intents.message_content = True  # Required for reading message content

# Set up the bot
bot = commands.Bot(command_prefix=["Z.","z.","zeon."], intents=intents)

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game('z.help'))
    print(f"✅ Logged in as {bot.user} (ID: {bot.user.id})")
    global logchannel
    logchannel = bot.get_channel(LOG_CHANNEL_ID)
    statuschannel = bot.get_channel(STATUS_CHANNEL_ID)

    if statuschannel:
        await statuschannel.send(f'<t:{int(time.time())}:f> Bot has started')
    else:
        print("⚠️ Could not find the channel to send startup message.")
    
@bot.event
async def on_message(message):
  if not message.author.bot and message.content.split(" ")[0] == f"<@{bot.user.id}>":
    ctx = await bot.get_context(message)
    await ctx.invoke(bot.get_command(name='help'))
    # await ctx.invoke(bot.get_command(name='speak'))

  if isinstance(message.channel, discord.channel.DMChannel) and not message.author.bot and not message.author.id in ADMIN_ID:
    output = f"**-->[DM]**`{message.author}`: {message.content}"
    print(output)
    await logchannel.send(output)
    if message.attachments:
    	outputattach = ", ".join([i.url for i in message.attachments])
    	await logchannel.send("Attachments: " + outputattach)
    
  await bot.process_commands(message)

@bot.command()
async def ping(ctx):
    """Pings the bot"""
    await ctx.send("🏓 Pong!")

#-------admin commands---------
@bot.command(hidden=True)
async def dm(ctx, userid: discord.User, *, text):
  if ctx.author.id in ADMIN_ID:
    print(userid)
    try:
      await userid.send(text)
      await logchannel.send(f"DM sent to {userid}")
    except:
      await logchannel.send(f"DM failed to send to {userid}")

if __name__ == "__main__":
    bot.run(TOKEN)
    