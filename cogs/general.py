import discord
from discord.ext import commands
import json


class General(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'General Cog Loaded Successfully!')

    @commands.command(name="Getprefix", help="Gets the current prefix for the server")
    async def getprefix(self, ctx):
        with open('./prefixes.json', 'r') as file:
            prefixes = json.load(file)

        await ctx.send(f'Get current prefix is: {prefixes[str(ctx.message.guild.id)]}')

    @commands.command(name="Ping", help="Pong!")
    async def ping(self, ctx):
        await ctx.send(f'Pong! {round(self.client.latency * 1000)}ms')


def setup(client):
    client.add_cog(General(client))
