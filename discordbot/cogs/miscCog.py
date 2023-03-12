import os
import discord
import discord.utils
from dotenv import load_dotenv
from pymongo import MongoClient
from discord.ext import commands
load_dotenv()


class MiscCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        env_dict = dict(os.environ)
        for key in env_dict:
            if key.startswith("DB_"):
                setattr(self, key, env_dict[key])

        self.db_url = getattr(self, "DB_URL", None)
        self.db_db = getattr(self, "DB_DB", None)

        self.client = MongoClient(self.db_url)
        self.db = self.client[self.db_db]

    @commands.command()
    async def muted(self, ctx):
        try: 
            usersMuted = next(self.db.mutedUsers.find())
        except StopIteration:
            embed = discord.Embed(color=discord.colour.Color.red())
            embed.set_author(name=f"{ctx.author}", icon_url=ctx.author.avatar)
            embed.add_field(name="Muted", value="No one is muted", inline=False)
            return await ctx.send(embed=embed)

        mutedUsers = []
        #get only values from the dict
        for key, value in usersMuted.items():
            if key == "usermuted":
                mutedUsers.append(value)
                continue
            elif key == "time":
                mutedUsers.append(str(value))
        embed = discord.Embed(color=0x00ff00)
        embed.set_author(name=f'{ctx.author.name}!', icon_url=ctx.author.avatar)
        embed.add_field(name="Muted Users", value=mutedUsers[0], inline=True)
        embed.add_field(name="Time Left", value=mutedUsers[1], inline=True)
        return await ctx.send(embed=embed)

    @commands.command()
    async def banned(self, ctx):
        try: 
            usersBanned = next(self.db.bannedUsers.find())
        except StopIteration:
            embed = discord.Embed(color=discord.colour.Color.red())
            embed.set_author(name=f"{ctx.author}", icon_url=ctx.author.avatar)
            embed.add_field(name="Banned", value="No one is banned", inline=False)
            return await ctx.send(embed=embed)
        
        bannedUsers = []
        #get only values from the dict
        for key, value in usersBanned.items():
            if key == "userbanned":
                bannedUsers.append(value)
                continue
        embed = discord.Embed(color=0x00ff00)
        embed.set_author(name=f'{ctx.author.name}!', icon_url=ctx.author.avatar)
        embed.add_field(name="Banned Users", value=bannedUsers, inline=True)
        return await ctx.send(embed=embed)
    
async def setup(bot):
    await bot.add_cog(MiscCommands(bot))