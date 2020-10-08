from discord.ext import commands
import discord
from main import client as bot


class General(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'General Cog Loaded Successfully!')

    @commands.command(name="Getprefix", help="Gets the current prefix for the server")
    async def getprefix(self, ctx):
        embed = discord.Embed()
        embed.add_field(name='The current prefix is:',
                        value=f'{await bot.get_prefix(ctx.message)}')
        await ctx.send(embed=embed)

    @commands.command(name="Ping", help="Get the current latency of the bot")
    async def ping(self, ctx):
        embed = discord.Embed(
            title="🏓 Pong!"
        )
        embed.set_footer(
            text=f'Latency: {round(self.client.latency * 1000)}ms'
        )
        await ctx.send(embed=embed)

    @commands.command(name="Invite", help="Get the invite link for the bot")
    async def invite(self, ctx):
        embed = discord.Embed()
        embed.set_thumbnail(url=self.client.user.avatar_url)
        embed.add_field(name='Use this link to invite me!',
                        value=f'https://discord.com/oauth2/authorize?client_id={bot.user.id}&scope=bot&permissions=8')
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(General(client))
