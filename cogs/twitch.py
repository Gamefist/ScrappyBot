import discord
from discord.ext import commands
import aiohttp


class Twitch(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Twitch Cog Loaded Successfully!')

    @commands.group(invoke_without_command=True)
    async def twitch(self, ctx):
        await ctx.send("Run !help twitch to get more information about the usage of this command!")

    @twitch.command(name="Status", help="Get the status of a twitch channel", aliases=["status"])
    async def status(self, ctx, channel):
        async with ctx.channel.typing():
            async with aiohttp.ClientSession() as session:
                async with session.get(f'https://decapi.me/twitch/uptime/{channel}') as request:
                    data = await request.text()
                    if "offline" in data:
                        await ctx.send(f'{channel} is Offline!')
                    else:
                        await ctx.send(f'{channel} is Online!')

    @status.error
    async def unban_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f'{ctx.message.author.mention} Please specify a twitch channel to get the status from.')


def setup(client):
    client.add_cog(Twitch(client))
