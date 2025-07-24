import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import speedtest

import time
import random

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
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
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

# Define a command that calls the default help command
@bot.command(name="info", aliases=["commands", "h", "helpmedaddy"])
async def help_alias(ctx):
    # Call the default help command with no arguments
    ctx.command = ctx.bot.get_command('help')  # Trick to set the context
    await ctx.bot.invoke(ctx)

@bot.command(help="Pings the bot.")
async def ping(ctx):
    # """Pings the bot"""
    await ctx.send("Pong!")
    
    
@bot.command(name="speedtest", help="Check host server's download and upload speeds.")
async def speedtest_command(ctx):
    await ctx.send("Running speed test... This may take up to 30 seconds.")
    try:
        st = speedtest.Speedtest()
        st.get_best_server()

        download_speed = st.download()  # bits per second
        upload_speed = st.upload()      # bits per second

        download_mbps = download_speed / 1_000_000
        upload_mbps = upload_speed / 1_000_000

        await ctx.send(
            f"**Speed Test Results**:\n"
            f"Download: **{download_mbps:.2f} Mbps**\n"
            f"Upload: **{upload_mbps:.2f} Mbps**"
        )

    except Exception as e:
        await ctx.send(f"⚠️ Speedtest failed: `{e}`")

@bot.command(name="choose", help="Randomly choose one option from a list.\nUsage: z.choose option1 option2 ...")
async def choose(ctx, *options):
    if not options:
        await ctx.send("⚠️ You need to give me some options to choose from!\nExample: `z.choose pizza burger sushi`")
    else:
        choice = random.choice(options)
        await ctx.send(f"🎲 I choose: **{choice}**")
        
@bot.command(name="8ball", aliases=["eightball", "magic8"], help="Ask the magic 8-ball a yes/no question.")
async def eight_ball(ctx, *, question: str = None):
    responses = [
        # Positive
        "It is certain.",
        "It is decidedly so.",
        "Without a doubt.",
        "Yes – definitely.",
        "You may rely on it.",
        "As I see it, yes.",
        "Most likely.",
        "Outlook good.",
        "Yes.",
        "Signs point to yes.",
        
        # Non-committal
        "Reply hazy, try again.",
        "Ask again later.",
        "Better not tell you now.",
        "Cannot predict now.",
        "Concentrate and ask again.",
        
        # Negative
        "Don't count on it.",
        "My reply is no.",
        "My sources say no.",
        "Outlook not so good.",
        "Very doubtful."
    ]

    answer = random.choice(responses)
    await ctx.send(f"{answer}")

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
    