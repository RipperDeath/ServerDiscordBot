import os
import discord
import asyncio
import datetime
import discord.utils
from pymongo import errors
from dotenv import load_dotenv
from pymongo import MongoClient
from discord.ext import commands
load_dotenv()

class ModErrorhandler(commands.Cog):
    async def kick_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please specify a member to kick.")
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send("You are not allowed to kick members.")

    async def ban_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please specify a member to ban.")
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send("You are not allowed to ban members.")

    async def mute_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please specify a member to mute.")
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send("You are not allowed to mute members.")

class Moderation(ModErrorhandler):
    def __init__(self, bot):
        self.bot = bot
        env_dict = dict(os.environ)# get the environment variables
        for key in env_dict: # get the variables that start with DB_
            if key.startswith("DB_"):
                setattr(self, key, env_dict[key]) # set the variables as attributes

        #get all the variables that start with DB_
        self.db_url = getattr(self, "DB_URL", None)

        #connect to the database
        self.client = MongoClient(self.db_url)

    @commands.command()
    async def kick(self, ctx, member: discord.Member, reason=None):

        guild = "".join([word[0].upper() + word[1:] for word in member.guild.name.lower().split("_")])
        self.db = self.client[guild]
        kickedUser = self.db["kickedUsers"]

        embed = discord.Embed(color=discord.colour.Color.red())
        embed.set_author(name=f"{ctx.author}", icon_url=ctx.author.avatar_url)
        embed.add_field(name="kick", value=f"{ctx.author} kicked {member.name}", inline=False)
        embed.add_field(name="Reason", value=reason, inline=False)
        await member.kick(reason=reason)
        kickedUser.insert_one({"_id": int(member.id), "author": str(ctx.author), "userkicked": member.name, "reason": reason})
        await ctx.send(embed=embed)

    @commands.command()
    async def ban(self, ctx, member: discord.Member, reason=None):

        guild = "".join([word[0].upper() + word[1:] for word in member.guild.name.lower().split("_")])
        self.db = self.client[guild]
        bannedUser = self.db["bannedUsers"]

        embed = discord.Embed(color=discord.colour.Color.red())
        embed.set_author(name=f"{ctx.author}", icon_url=ctx.author.avatar_url)
        embed.add_field(name="ban", value=f"{ctx.author} banned {member.name}", inline=False)
        embed.add_field(name="Reason", value=reason, inline=False)
        await member.ban(reason=reason)
        bannedUser.insert_one({"_id": int(member.id), "author": str(ctx.author), "userbanned": f"{member.name}#"+f"{member.discriminator}", "reason": reason, "date": datetime.datetime.utcnow()})
        await ctx.send(embed=embed)

    @commands.command()
    async def unban(self, ctx, *, member):

        guild = "".join([word[0].upper() + word[1:] for word in member.guild.name.lower().split("_")])
        self.db = self.client[guild]
        bannedUser = self.db["bannedUsers"]

        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')
        for ban_entry in banned_users:
            user = ban_entry.user
            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                embed = discord.Embed(color=discord.colour.Color.green())
                embed.set_author(name=f"{ctx.author}", icon_url=ctx.author.avatar_url)
                embed.add_field(name="unban", value=f"{ctx.author} unbanned {user.name}", inline=False)
                bannedUser.delete_one({"_id": user.id})
                await ctx.send(embed=embed)

    @commands.command()
    async def mute(self, ctx, member: discord.Member, reason=None, time=0):
        embed = discord.Embed(color=discord.colour.Color.red())
        embed.set_author(name=f"{ctx.author}", icon_url=ctx.author.avatar_url)
        embed.add_field(name="mute", value=f"{ctx.author} muted {member.name}", inline=False)
        embed.add_field(name="Reason", value=reason, inline=False)
        embed.add_field(name="Time", value=time, inline=False)
        await ctx.send(embed=embed)
        #give muted role to user and remove sending messages permission
        mutedRole = discord.utils.get(ctx.guild.roles, name="muted")
        await member.add_roles(mutedRole)
        #adds user to the database
        try:
            print(member.guild.name)
            #set first char in guild name to uppercase exept the first character
            guild = "".join([word[0].upper() + word[1:] for word in member.guild.name.lower().split(" ")])
            #make first character of guild name lowercase
            guild = guild[0].lower() + guild[1:]
            self.db = self.client[guild]
            post = {"_id": int(member.id), "author": str(ctx.author), "usermuted": str(member.name+"#"+member.discriminator), "reason": reason, "time": time, "date": datetime.datetime.utcnow()}
            coll = self.db["mutedUsers"]
        except Exception as e:
            print(e)
            return

        print("adding to db")
        try: #i forgot what this try statement is for
            try: #trys to add user to the database
                coll.insert_one(post)
            except errors.DuplicateKeyError: #if user is already in the database, then update user
                print("duplicate key error")
                coll.update_one({"_id": int(member.id)}, {"$set": {"author": str(ctx.author), "usermuted": str(member.name+"#"+member.discriminator), "reason": reason, "time": time, "date": datetime.datetime.utcnow()}})
        except Exception as e:
            print(e)
        #timer to remove muted role
        await asyncio.sleep(time)
        await member.remove_roles(mutedRole)
        coll.delete_one({"_id": int(member.id)})

    @commands.command()
    async def unmute(self, ctx, member: discord.Member):

        guild = "".join([word[0].upper() + word[1:] for word in member.guild.name.lower().split("_")])
        self.db = self.client[guild]
        mutedUser = self.db["mutedUsers"]

        embed = discord.Embed(color=discord.colour.Color.green())
        embed.set_author(name=f"{ctx.author}", icon_url=ctx.author.avatar_url)
        embed.add_field(name="unmute", value=f"{ctx.author} unmuted {member.name}", inline=False)
        await member.remove_roles(discord.utils.get(ctx.guild.roles, name="muted"))
        mutedUser.delete_one({"_id": member.id})
        await ctx.send(embed=embed)

    #section is for error handling cause of retards
    @kick.error
    async def kick_error(self, ctx, error):
        ModErrorhandler.kick_error(self, ctx, error)

    @ban.error
    async def ban_error(self, ctx, error):
        ModErrorhandler.ban_error(self, ctx, error)

    @mute.error
    async def mute_error(self, ctx, error):
        ModErrorhandler.mute_error(self, ctx, error)

def setup(bot):
    bot.add_cog(Moderation(bot))