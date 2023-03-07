import os
import json
import asyncio
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

startup_extensions = []
#loops through all the extensions
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        startup_extensions.append("cogs."+filename[:-3]) #removes .py from filename

# starting extensions
for extension in startup_extensions:
    try:
        bot.load_extension(extension)
        print(f"{extension} loaded")
    except Exception as e:
        exc = '{}: {}'.format(type(e).__name__, e)
        print(f'Failed to load extension {extension}\n{exc}')

@bot.event
async def on_ready():
    print(f"{bot.user} is now online!")
    uptime.start()

# uptime counter
@tasks.loop(seconds=1)
async def uptime(): #uptime
    await bot.wait_until_ready()
    timeCounter = 0
    counter = 0
    while not bot.is_closed():
        counter += 1
        timeCounter += 1
        #convert seconds to days, hours, minutes, seconds
        days = int(timeCounter / 86400)
        hours = int(timeCounter / 3600) % 24
        minutes = int(timeCounter / 60) % 60
        seconds = timeCounter % 60

        await asyncio.sleep(1)
        if counter == 60:
            print(f"Uptime: {days} days, {hours} hours, {minutes} minutes, {seconds} seconds")
            counter = 0

env_dict = dict(os.environ) #supposally this is faster than a regular call to os.environ
#bot.loop.create_task(uptime())
bot.run(env_dict['TESTBOT'])
