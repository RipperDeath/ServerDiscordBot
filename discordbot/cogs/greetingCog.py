import os
import discord
import discord.utils
from dotenv import load_dotenv
from pymongo import MongoClient
from discord.ext import commands
load_dotenv()

class Greetings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
        
        env_dict = dict(os.environ)
        for key in env_dict:
            if key.startswith("DB_"):
                setattr(self, key, env_dict[key])

        self.db_url = getattr(self, "DB_URL", None)

        self.client = MongoClient(self.db_url)

    @commands.Cog.listener()
    async def on_member_join(self, member):

        guild = "".join([word[0].upper() + word[1:] for word in member.guild.name.lower().split(" ")])
        self.db = self.client[guild]

        for channel in member.guild.channels:
            if channel.name == "general":
                general = channel.id
                break

        channel = member.guild.system_channel
        if channel is not None:
            embed = discord.Embed(color=0x00ff00)
            embed.set_author(name=f'{member.name}!', icon_url=member.avatar)
            embed.set_thumbnail(url=member.guild.icon_url)
            await channel.send(embed=embed)
        role = discord.utils.get(member.guild.roles, name="test1")
        print(f"{member}: has added role: {role}")
        await member.add_roles(role)
        #if user is in db then raise eyebrow, throw caution (# number of times user has been kicked) specified when user was kicked
        if member.id == self.db[guild+"_KickedUsers"].find_one({"_id": member.id})["_id"]:
            await general.send("I got my eye on you bud" + member.mention)
        else: #user is a good boi!
            pass

    @commands.Cog.listener()
    async def on_message(self, message):
        guild = "".join([word[0].upper() + word[1:] for word in message.guild.name.lower().split(" ")])
        self.db = self.client[guild]

        if message.author == self.bot.user or message.author.bot:
            return
        
        print(f'{message.author} in {message.channel}: {message.content}')

async def setup(bot):
    await bot.add_cog(Greetings(bot))