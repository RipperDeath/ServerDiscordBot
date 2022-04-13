import token
import discord
#from discord import Webhook, AsyncWebhookAdapter
import datetime
from pytz import timezone
import asyncio




#TODO
#1. fix embed /fixed
#2. fix role picker /fixed
#3. add colors for role selection 
#4. 

class MyClient(discord.Client):
  async def on_ready(self):
    print('Logged on as {0}!'.format(self.user))
    return "logged in"

  async def on_message(self, message):
    timeNow = datetime.datetime.now(timezone('US/Eastern')).strftime("%m-%d-%Y %H:%M:%S")
    #stops bot spam
    if message.author == client.user or message.author.bot:
      return
    print(f'[{timeNow}] {message.author} in {message.channel}: {message.content}')
    return self.message.author, self.message.content

  #sends a welcome embed message to welcome
  async def on_member_join(self, member):
    #chWelcome = client.get_channel(875945037077299241)
    channel = discord.utils.get(member.guild.text_channels, id=875945037077299241)
    print(channel)
    #embed = discord.Embed(title="text", description=f"{member.mention} text", color=0x220d4d)
    #await channel.send(embed=embed)
    guild = channel.guild
    role = discord.utils.get(guild.roles, name='superstar')
    await member.add_roles(role)
    return member

  #Role selection add
  async def on_raw_reaction_add(self, payload):
    if payload.message_id == 936888553319849984:
      channel = client.get_channel(payload.channel_id)
      message = await channel.fetch_message(payload.message_id)
      guildId = payload.guild_id
      guild = discord.utils.find(lambda g : g.id == guildId, client.guilds)
      memeber = await guild.fetch_member(payload.user_id)
      #print(message)
      print(payload.emoji)
      if payload.emoji.name == 'producer':
         print(payload.emoji.name)
         role = discord.utils.get(guild.roles, name='PRODUCER')
      elif payload.emoji.name == 'artists':
         role = discord.utils.get(guild.roles, name="ARTIST")
      else:
         await message.remove_reaction(payload.emoji, memeber)
         print(f'cleared emoji {payload.emoji}')
      #role = None
      if role is not None:
         if memeber is not None:
            await memeber.add_roles(role)
            print(f"{memeber}: has added role: {role}")
            return f"{memeber}: has added role: {role}"
         else:
            print('memeber not found')
      else:
          print(f'{memeber}: Add Role not found')

  #Role selection remove
  async def on_raw_reaction_remove(self, payload):
    messageId = payload.message_id
    if messageId == 936888553319849984:
      guildId = payload.guild_id
      guild = discord.utils.find(lambda g: g.id == guildId, client.guilds)
      if payload.emoji.name == 'producer':
        role = discord.utils.get(guild.roles, name='PRODUCER')
      elif payload.emoji.name == 'artists':
        role = discord.utils.get(guild.roles, name="ARTIST")
      else:
        return
      if role is not None:
        memeber = await guild.fetch_member(payload.user_id)
        if memeber is not None:
          await memeber.remove_roles(role)
          print(f"{memeber}: has removed role: {role}")
          return f"{memeber}: has removed role: {role}"
        else:
          print('memeber not found')
      else:
        print('Remeove Role not found')    

async def printDateLogs():
  #adds a date on space to make logs more pretty lookning
  while(True):
    tz = timezone('US/Eastern')
    if datetime.datetime.now(timezone('US/Eastern')).strftime("%H:%M:%S") == "24:0:05":
      f = open("messages.txt", "a")
      f.write('-->{0}<--\n'.format(datetime.datetime.now(tz).strftime("%m/%d/%y")))
      print("printed day in txt")
      f.close()
    await asyncio.sleep(1)

client = MyClient()
client.loop.create_task(printDateLogs())
client.run(token)