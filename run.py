import os
import json
import asyncio
import datetime, time
import discord
from dotenv import load_dotenv
from discord.ext import commands, tasks
load_dotenv()

# get stuff from config.json instead of hardcoding
with open('config.json') as f:
    config = json.load(f)
    prefix = config['prefix']

bot = commands.Bot(command_prefix=prefix, intents=discord.Intents.all()) #fuck it, idk what i need
bot.remove_command("help")

async def load_extensions():
    startup_extensions = []
    #loops through all the extensions
    for filename in os.listdir('./discordbot/cogs'):
        if filename.endswith('.py'):
            startup_extensions.append("discordbot.cogs."+filename[:-3]) #removes .py from filename

    # starting extensions
    for extension in startup_extensions:
        try:
            await bot.load_extension(extension)
            print(f"{extension} loaded")
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print(f'Failed to load extension {extension}\n{exc}')

@bot.event
async def on_ready():
    print(f"{bot.user} is now online!")
    starttime = time.time()
    try:
        uptime.start(starttime)
    except RuntimeError:
        pass

# uptime counter
@tasks.loop(seconds=60)
async def uptime(starttime): #uptime
    print(f"Bot uptime: {datetime.timedelta(seconds=int(round(time.time()-starttime)))}")

env_dict = dict(os.environ) #supposally this is faster than a regular call to os.environ
#bot.loop.create_task(uptime())
asyncio.run(load_extensions())
bot.run(env_dict['TESTBOT'])
