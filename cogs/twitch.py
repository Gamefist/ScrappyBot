import discord
from discord.ext import commands
import aiohttp
from main import client as bot

class Twitch(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Twitch Cog Loaded Successfully!')

    @commands.group(invoke_without_command=True)
    async def twitch(self, ctx, channel):
        async with ctx.channel.typing():
            async with aiohttp.ClientSession() as session:
                async with session.get(f'https://decapi.me/twitch/avatar/{channel}') as request:
                    data = await request.text()
                    if "User not found" in data:
                        embed = discord.Embed()
                        embed.add_field(name=data, value=f'** **', inline=False)
                    else:
                        thumbnail = data
                        async with session.get(f'https://decapi.me/twitch/uptime/{channel}') as request:
                            data = await request.text()
                            embed = discord.Embed(title=f'Twitch channel: {channel}')
                            if "offline" in data:
                                embed.set_thumbnail(url=thumbnail)
                                embed.add_field(name=f'Status:', value=f'Offline', inline=True)
                            else:
                                embed.set_thumbnail(url=thumbnail)
                                async with session.get(f'https://decapi.me/twitch/status/{channel}') as request:
                                    data = await request.text()
                                    embed.add_field(name=f'Title:', value=data,
                                                    inline=False)
                                async with session.get(f'https://decapi.me/twitch/game/{channel}') as request:
                                    data = await request.text()
                                    embed.add_field(name=f'Currently playing:', value=data,
                                                    inline=False)
                                embed.add_field(name=f'Status:', value=f'Online', inline=True)
                                async with session.get(f'https://decapi.me/twitch/viewercount/{channel}') as request:
                                    data = await request.text()
                                    embed.add_field(name=f'Viewers:', value=data, inline=True)
                            async with session.get(f'https://decapi.me/twitch/followcount/{channel}') as request:
                                data = await request.text()
                                embed.add_field(name=f'Followers:', value=data, inline=True)
                            async with session.get(f'https://decapi.me/twitch/accountage/{channel}') as request:
                                data = await request.text()
                                embed.add_field(name=f'Account age: ', value=data, inline=False)
                            async with session.get(f'https://decapi.me/twitch/chat_rules/{channel}') as request:
                                data = await request.text()
                                embed.add_field(name=f'Chat rules:', value=data, inline=False)
                    embed.set_footer(text=f'For more information type {await bot.get_prefix(ctx.message)}help twitch',
                                     icon_url=self.client.user.avatar_url)
                    await ctx.send(embed=embed)

    @twitch.error
    async def twitch_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f'{ctx.message.author.mention} Please specify a twitch channel and/or subcommand. \n'
                           f'You can also run !help twitch for additional information!')

    @twitch.command(name="Status", help="Get the status of a specified twitch channel", aliases=["status"])
    async def status(self, ctx, channel):
        async with ctx.channel.typing():
            async with aiohttp.ClientSession() as session:
                async with session.get(f'https://decapi.me/twitch/uptime/{channel}') as request:
                    data = await request.text()
                    embed = discord.Embed()
                    if "offline" in data:
                        embed.add_field(name=f'{channel} is currently:', value=f'Offline', inline=False)
                    else:
                        embed.add_field(name=f'{channel} is currently:', value=f'Online', inline=False)
                    await ctx.send(embed=embed)

    @status.error
    async def status_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f'{ctx.message.author.mention} Please specify a twitch channel to get the status from.')

    @twitch.command(name="Age", help="Get the age of a specified twitch channel", aliases=["age"])
    async def age(self, ctx, channel):
        async with ctx.channel.typing():
            async with aiohttp.ClientSession() as session:
                async with session.get(f'https://decapi.me/twitch/accountage/{channel}') as request:
                    data = await request.text()
                    embed = discord.Embed()
                    if "No user with the name" in data:
                        embed.add_field(name=data, value=f'** **', inline=False)
                    else:
                        embed.add_field(name=f'{channel} has been streaming for: ', value=data, inline=False)
                    await ctx.send(embed=embed)

    @age.error
    async def age_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f'{ctx.message.author.mention} Please specify a twitch channel to get the age from.')

    @twitch.command(name="Avatar", help="Get the avatar of a specified twitch channel", aliases=["avatar"])
    async def avatar(self, ctx, channel):
        async with ctx.channel.typing():
            async with aiohttp.ClientSession() as session:
                async with session.get(f'https://decapi.me/twitch/avatar/{channel}') as request:
                    data = await request.text()
                    if "User not found" in data:
                        embed = discord.Embed()
                        embed.add_field(name=data, value=f'** **', inline=False)
                    else:
                        embed = discord.Embed(title=f'Twitch avatar of: {channel}')
                        embed.set_image(url=data)
                    await ctx.send(embed=embed)

    @avatar.error
    async def avatar_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f'{ctx.message.author.mention} Please specify a twitch channel to get the avatar from.')

    @twitch.command(name="Rules", help="Get the chat rules of a specified twitch channel", aliases=["rules"])
    async def rules(self, ctx, channel):
        async with ctx.channel.typing():
            async with aiohttp.ClientSession() as session:
                async with session.get(f'https://decapi.me/twitch/chat_rules/{channel}') as request:
                    data = await request.text()
                    embed = discord.Embed()
                    if "not found" in data:
                        embed.add_field(name=data, value=f'** **', inline=False)
                    else:
                        embed.add_field(name=f'Chat rules from: {channel}', value=data, inline=False)
                    await ctx.send(embed=embed)

    @rules.error
    async def rules_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f'{ctx.message.author.mention} Please specify a twitch channel to get the chat rules from.')

    @twitch.command(name="FollowCount", help="Get the amount of users following a specified twitch channel",
                    aliases=["followcount"])
    async def followcount(self, ctx, channel):
        async with ctx.channel.typing():
            async with aiohttp.ClientSession() as session:
                async with session.get(f'https://decapi.me/twitch/followcount/{channel}') as request:
                    data = await request.text()
                    embed = discord.Embed()
                    if "No user with the name" in data:
                        embed.add_field(name=data, value=f'** **', inline=False)
                    else:
                        embed.add_field(name=f'Users following {channel}:', value=data, inline=False)
                    await ctx.send(embed=embed)

    @followcount.error
    async def followcount_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f'{ctx.message.author.mention} Please specify a twitch channel to get the followcount from.')

    @twitch.command(name="Followers", help="Get the <amount> latest users following a specified twitch channel",
                    aliases=["followers"])
    async def followers(self, ctx, channel, amount: int):
        async with ctx.channel.typing():
            async with aiohttp.ClientSession() as session:
                async with session.get(f'https://decapi.me/twitch/followers/{channel}'
                                       f'?count={amount}?display_name') as request:
                    data = await request.text()
                    data = data.split(", ")
                    embed = discord.Embed()
                    if "No user with the name" in data[0]:
                        embed.add_field(name=data[0], value=f'** **', inline=False)
                    else:
                        users = ""
                        for user in data:
                            users += f'- {user} \n'
                        if amount == 1:
                            embed.add_field(name=f'Last user following {channel}:', value=users, inline=False)
                        else:
                            embed.add_field(name=f'Last {amount} users following {channel}:', value=users, inline=False)
                    await ctx.send(embed=embed)

    @followers.error
    async def followers_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            if error.param.name == 'amount':
                await ctx.send(f'{ctx.message.author.mention} Please specify the amount of '
                               f'followers you are trying to retrieve.')
            else:
                await ctx.send(f'{ctx.message.author.mention} Please specify a twitch channel to get the '
                               f'followers from.')

    @twitch.command(name="Game", help="Get the current game a specified twitch channel is playing", aliases=["game"])
    async def game(self, ctx, channel):
        async with ctx.channel.typing():
            async with aiohttp.ClientSession() as session:
                async with session.get(f'https://decapi.me/twitch/game/{channel}') as request:
                    data = await request.text()
                    embed = discord.Embed()
                    if "No user with the name" in data:
                        embed.add_field(name=data, value=f'** **', inline=False)
                    else:
                        embed.add_field(name=f'{channel} is currently playing:', value=data, inline=False)
                    await ctx.send(embed=embed)

    @game.error
    async def game_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f'{ctx.message.author.mention} Please specify a twitch channel to get the '
                           f'current game from.')

    @twitch.command(name="Highlight", help="Get the latest hightlight from a specified "
                                           "twitch channel", aliases=["highlight"])
    async def highlight(self, ctx, channel):
        async with ctx.channel.typing():
            async with aiohttp.ClientSession() as session:
                async with session.get(f'https://decapi.me/twitch/highlight/{channel}') as request:
                    data = await request.text()
                    embed = discord.Embed()
                    if "No user with the name" in data:
                        embed.add_field(name=data, value=f'** **', inline=False)
                    else:
                        embed.add_field(name=f'Latest highlight from {channel}:', value=data, inline=False)
                    await ctx.send(embed=embed)

    @highlight.error
    async def highlight_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f'{ctx.message.author.mention} Please specify a twitch channel to get the '
                           f'latest highlight from.')

    @twitch.command(name="Hosts", help="Get the channels currently hosting "
                                       "the specified twitch channel", aliases=["hosts"])
    async def hosts(self, ctx, channel):
        async with ctx.channel.typing():
            async with aiohttp.ClientSession() as session:
                async with session.get(f'https://decapi.me/twitch/hosts/{channel}?display_name') as request:
                    data = await request.json()
                    embed = discord.Embed()
                    if data:
                        channels = ''
                        for hostingChannel in data:
                            channels += f'- {hostingChannel} \n'
                        embed.add_field(name=f'Channels currently hosting: {channel}', value=channels, inline=False)
                    else:
                        embed.add_field(name=f'No-one is currently hosting this channel.', value=f'** **', inline=False)
                    await ctx.send(embed=embed)

    @hosts.error
    async def hosts_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f'{ctx.message.author.mention} Please specify a twitch channel to get the '
                           f'list of hosts from.')

    @twitch.command(name="ID", help="Get the Twitch user ID from a specified user (if valid)", aliases=["id"])
    async def id(self, ctx, user):
        async with ctx.channel.typing():
            async with aiohttp.ClientSession() as session:
                async with session.get(f'https://decapi.me/twitch/id/{user}') as request:
                    data = await request.text()
                    embed = discord.Embed()
                    if "not found" in data:
                        embed.add_field(name=data, value=f'** **', inline=False)
                    else:
                        embed.add_field(name=f'Twitch user ID of {user}:', value=data, inline=False)
                    await ctx.send(embed=embed)

    @id.error
    async def id_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f'{ctx.message.author.mention} Please specify the user to get the '
                           f'Twitch user ID from.')

    @twitch.command(name="RandomUser", help="Get a random user currently in the specified Twitch channel's chat",
                    aliases=["randomuser"])
    async def randomuser(self, ctx, channel):
        async with ctx.channel.typing():
            async with aiohttp.ClientSession() as session:
                async with session.get(f'https://decapi.me/twitch/random_user/{channel.lower()}') as request:
                    data = await request.text()
                    embed = discord.Embed()
                    if "The list of users is empty." in data:
                        embed.add_field(name=data, value=f'** **', inline=False)
                    else:
                        embed.add_field(name=f'Random user:', value=data, inline=False)
                    await ctx.send(embed=embed)

    @randomuser.error
    async def randomuser_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f'{ctx.message.author.mention} Please specify the channel to get a random user from.')

    @twitch.command(name="Title", help="Get the current title set on a specified Twitch channel",
                    aliases=['title'])
    async def title(self, ctx, channel):
        async with ctx.channel.typing():
            async with aiohttp.ClientSession() as session:
                async with session.get(f'https://decapi.me/twitch/status/{channel}') as request:
                    data = await request.text()
                    embed = discord.Embed()
                    if data:
                        embed.add_field(name=f'Current title of {channel}:', value=data, inline=False)
                    else:
                        embed.add_field(name=f'Channel: {channel} not found', value=f'** **', inline=False)
                    await ctx.send(embed=embed)

    @title.error
    async def title_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f'{ctx.message.author.mention} Please specify the channel to get the title from.')

    @twitch.command(name="TotalViews", help="Get the total views a specified Twitch channel has",
                    aliases=['totalviews', 'views'])
    async def totalviews(self, ctx, channel):
        async with ctx.channel.typing():
            async with aiohttp.ClientSession() as session:
                async with session.get(f'https://decapi.me/twitch/total_views/{channel}') as request:
                    data = await request.text()
                    embed = discord.Embed()
                    if "User not found:" in data:
                        embed.add_field(name=data, value=f'** **', inline=False)
                    else:
                        embed.add_field(name=f'Total views:', value=data, inline=False)
                    await ctx.send(embed=embed)

    @totalviews.error
    async def totalviews_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f'{ctx.message.author.mention} Please specify the channel to get the total views from.')

    @twitch.command(name="LatestUpload", help="Get the latest upload from a specified Twitch channel has",
                    aliases=['upload', 'latestupload'])
    async def latestupload(self, ctx, channel):
        async with ctx.channel.typing():
            async with aiohttp.ClientSession() as session:
                async with session.get(f'https://decapi.me/twitch/upload/{channel}') as request:
                    data = await request.text()
                    if "No user with the name" in data:
                        embed = discord.Embed()
                        embed.add_field(name=data, value=f'** **', inline=False)
                        await ctx.send(embed=embed)
                    elif "has no uploaded videos" in data:
                        embed = discord.Embed()
                        embed.add_field(name=data, value=f'** **', inline=False)
                        await ctx.send(embed=embed)
                    else:
                        await ctx.send(data)

    @latestupload.error
    async def latestupload_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f'{ctx.message.author.mention} Please specify the channel to get the latest upload from.')

    @twitch.command(name="Uptime", help="Get the uptime from a specified Twitch channel",
                    aliases=['uptime', 'time'])
    async def uptime(self, ctx, channel):
        async with ctx.channel.typing():
            async with aiohttp.ClientSession() as session:
                async with session.get(f'https://decapi.me/twitch/uptime/{channel}') as request:
                    data = await request.text()
                    embed = discord.Embed()
                    embed.add_field(name=f'Uptime of {channel}:', value=data, inline=False)
                    await ctx.send(embed=embed)

    @uptime.error
    async def uptime_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f'{ctx.message.author.mention} Please specify the channel to get the uptime from.')

    @twitch.command(name="Viewercount", help="Get the current amount of viewers a specified Twitch channel has",
                    aliases=['viewercount', 'viewers', 'viewcount'])
    async def viewercount(self, ctx, channel):
        async with ctx.channel.typing():
            async with aiohttp.ClientSession() as session:
                async with session.get(f'https://decapi.me/twitch/viewercount/{channel}') as request:
                    data = await request.text()
                    embed = discord.Embed()
                    if "No user with the name" in data:
                        embed.add_field(name=data, value=f'** **', inline=False)
                    else:
                        embed.add_field(name=f'Current amount of viewers:', value=data, inline=False)
                    await ctx.send(embed=embed)

    @viewercount.error
    async def viewercount_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f'{ctx.message.author.mention} Please specify the channel to get the viewercount from.')


def setup(client):
    client.add_cog(Twitch(client))
