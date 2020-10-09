import discord
import mysql.connector
from discord.ext import commands
from main import client as bot
from database import db

logChannel = 753963587898310716


async def is_it_me(ctx):
    return ctx.author.id == 598602545023418380


class Administration(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Administration Cog Loaded Successfully!')

    @commands.command(name="Clear", help="Clear <amount> of messages", aliases=['Purge'])
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount: int):
        await ctx.channel.purge(limit=amount)

    @clear.error
    async def clear_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f'{ctx.message.author.mention} Please specify the number of messages you wish to delete')
        if isinstance(error, commands.BadArgument):
            await ctx.send(f'{ctx.message.author.mention} Please only specify '
                           f'the number of messages you wish to delete')

    @commands.command(name="Kick", help="Kick a user")
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        await member.kick(reason=reason)
        await ctx.send(f'Kicked {member.mention}')

    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f'{ctx.message.author.mention} Please mention the member you wish to kick from the server')

    @commands.command(name="Ban", help="Ban a user")
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        await member.ban(reason=reason)
        await ctx.send(f'Banned {member.mention}')

    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f'{ctx.message.author.mention} Please mention the member you wish to ban from the server')

    @commands.command(name="Unban", help="Unban a user")
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, *, member):
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')
        for ban_entry in banned_users:
            user = ban_entry.user

            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.send(f'Unbanned {user.mention}')
                return

    @unban.error
    async def unban_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f'{ctx.message.author.mention} Please specify the member you wish to unban from the server')

    @commands.command(name="Load", help="Load an extension")
    @commands.check(is_it_me)
    async def load(self, ctx, extension):
        self.client.load_extension(f'cogs.{extension}')
        await ctx.message.add_reaction('✅')

    @commands.command(name="Unload", help="Unload an extension")
    @commands.check(is_it_me)
    async def unload(self, ctx, extension):
        self.client.unload_extension(f'cogs.{extension}')
        await ctx.message.add_reaction('✅')

    @commands.command(name="Reload", help="Reload an extension")
    @commands.check(is_it_me)
    async def reload(self, ctx, extension):
        self.client.unload_extension(f'cogs.{extension}')
        self.client.load_extension(f'cogs.{extension}')
        await ctx.message.add_reaction('✅')

    @commands.command(name="Setprefix", help="Changes the prefix for the server")
    @commands.has_permissions(manage_guild=True)
    async def setprefix(self, ctx, prefix):
        try:
            cursor = db.cursor()
            cursor.execute(f'UPDATE Guilds SET Prefix = "{prefix}" WHERE Guild_ID = {ctx.guild.id}')
            db.commit()
            bot.command_prefix = prefix
        except mysql.connector.Error as err:
            print("Something went wrong: {}".format(err))

        await ctx.message.add_reaction('✅')

    @setprefix.error
    async def setprefix_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f'{ctx.message.author.mention} Please specify the new prefix you wish to set for the server')

    @commands.command(name="Kill", help="Kill the bot")
    @commands.is_owner()
    async def kill(self, ctx):
        await ctx.message.add_reaction('✅')
        await bot.get_channel(logChannel).send(f'🤖 | {bot.user.display_name} is logging out...')
        bot.logout()


def setup(client):
    client.add_cog(Administration(client))
