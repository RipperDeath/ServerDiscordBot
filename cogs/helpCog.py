import discord
from discord.ext import commands

#Misc. help commands
class MiscHelpCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def muted(self, ctx):
        embed = discord.Embed(title=f"Muted", description="Shows list of muted users and how long they were muted for", color=discord.colour.Color.red())
        embed.set_author(name=f"{ctx.author}", icon_url=ctx.author.avatar)
        embed.add_field(name="muted", value=self.bot.command_prefix+"muted", inline=False)
        embed.set_footer(text="' = required")
        await ctx.send(embed=embed)

#Moderation help commands
class ModHelpCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    async def kick(self, ctx):
        embed = discord.Embed(title="Kick", description="This is a Kick command", color=discord.colour.Color.red())
        embed.set_author(name=f"{ctx.author}", icon_url=ctx.author.avatar)
        embed.add_field(name="kick", value=self.bot.command_prefix+"kick <member'> [reason']", inline=False)
        embed.set_footer(text="' = required")
        await ctx.send(embed=embed)

    async def ban(self, ctx):
        embed = discord.Embed(title="Ban", description="This is a Ban command", color=discord.colour.Color.red())
        embed.set_author(name=f"{ctx.author}", icon_url=ctx.author.avatar)
        embed.add_field(name="ban", value=self.bot.command_prefix+"ban <member'> [reason']", inline=False)
        embed.set_footer(text="' = required")
        await ctx.send(embed=embed)

    async def mute(self, ctx):
        embed = discord.Embed(title="Mute", description="This is a Mute command", color=discord.colour.Color.red())
        embed.set_author(name=f"{ctx.author}", icon_url=ctx.author.avatar)
        embed.add_field(name="mute", value=self.bot.command_prefix+"mute <member'> [reason'] [time(in seconds)']", inline=False)
        embed.set_footer(text="' = required")
        await ctx.send(embed=embed)

#Main help depot, inherits from classes above
class HelpCommands(MiscHelpCommands, ModHelpCommands):
    def __init__(self, bot):
        self.bot = bot
        super().__init__(bot)
    @commands.group(invoke_without_command=True)
    async def help(self, ctx):
        embed = discord.Embed(title="Help", description="This is a help command", color=discord.colour.Color.blue())
        embed.set_author(name=f"{ctx.author}", icon_url=ctx.author.avatar)
        embed.add_field(name="Moderation Usage", value="Kick, Ban, Mute", inline=False)
        embed.add_field(name="Misc", value="muted", inline=False)
        await ctx.send(embed=embed)

    @help.command()
    async def kick(self, ctx):
        await ModHelpCommands.kick(self, ctx)

    @help.command()
    async def ban(self, ctx):
        await ModHelpCommands.ban(self, ctx)

    @help.command()
    async def mute(self, ctx):
        await ModHelpCommands.mute(self, ctx)

    @help.command()
    async def muted(self, ctx):
        await MiscHelpCommands.muted(self, ctx)
    
    #error handling for useless people typing non-existent commands
    @help.error
    async def help_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(title="Invalid command", description="Please retry with one of the commands listed below", color=discord.colour.Color.blue())
            embed.set_author(name="Help", icon_url=ctx.author.avatar)
            embed.add_field(name="Moderation Usage", value="Kick, Ban, Mute", inline=False)
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(HelpCommands(bot))