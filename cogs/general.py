from discord.ext import commands

from main import client as bot


class General(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'General Cog Loaded Successfully!')

    @commands.command(name="Getprefix", help="Gets the current prefix for the server")
    async def getprefix(self, ctx):
        await ctx.send(f'The current prefix is: {await bot.get_prefix(ctx.message)}')

    @commands.command(name="Ping", help="Pong!")
    async def ping(self, ctx):
        await ctx.send(f'Pong! {round(self.client.latency * 1000)}ms')

    @commands.command(name="Invite", help="Get the invite link for the bot")
    async def invite(self, ctx):
        await ctx.send(f'Use this link to invite me! \n'
                       f'https://discord.com/oauth2/authorize?client_id={bot.user.id}&scope=bot&permissions=8')


def setup(client):
    client.add_cog(General(client))
