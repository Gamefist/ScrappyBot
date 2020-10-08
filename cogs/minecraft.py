import discord
from discord.ext import commands
import aiohttp


class Minecraft(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Minecraft Cog Loaded Successfully!')

    @commands.command(name="Server", help="Get information about a minecraft server")
    async def server(self, ctx, server):
        async with ctx.channel.typing():
            async with aiohttp.ClientSession() as session:
                async with session.get(f'https://api.mcsrvstat.us/2/{server}') as request:
                    data = await request.json()
                    if data['online']:
                        embed = discord.Embed(title=f'Minecraft Server: {server}')
                        embed.add_field(name=f'Server Status:', value=f'Online', inline=False)
                        embed.add_field(name=f'Description:', value=f'{data["motd"]["clean"][0]}\n'
                                                                    f'{data["motd"]["clean"][1]}', inline=False)
                        embed.add_field(name="Players:", value=f'Online: **{data["players"]["online"]}**\n '
                                                               f'Maximum: **{data["players"]["max"]}**', inline=True)
                        embed.add_field(name="Version:", value=f'{data["version"]}', inline=True)
                        embed.set_thumbnail(url=f'https://eu.mc-api.net/v3/server/favicon/{server}')
                        embed.set_footer(text='Server information by Scrappy', icon_url=self.client.user.avatar_url)
                        await ctx.send(embed=embed)
                    else:
                        embed = discord.Embed(title=f'Minecraft Server: {server}')
                        embed.add_field(name=f'Server Status:', value=f'Offline', inline=False)
                        embed.set_footer(text='Server information by Scrappy', icon_url=self.client.user.avatar_url)
                        await ctx.send(embed=embed)

    @commands.command(name="Skin", help="Get the minecraft skin from a username")
    async def skin(self, ctx, username):
        async with ctx.channel.typing():
            async with aiohttp.ClientSession() as session:
                async with session.get(f'https://playerdb.co/api/player/minecraft/{username}') as request:
                    data = await request.json()
                    if data['code'] == "player.found":
                        embed = discord.Embed(title=f'Minecraft skin of: \n{data["data"]["player"]["username"]}')
                        embed.set_image(url=f'https://crafatar.com/renders/body/{data["data"]["player"]["id"]}?overlay')
                        embed.set_footer(text='Skin lookup by Scrappy', icon_url=self.client.user.avatar_url)
                        await ctx.send(embed=embed)
                    else:
                        await ctx.send("Sorry this minecraft user could not be found!")


def setup(client):
    client.add_cog(Minecraft(client))
