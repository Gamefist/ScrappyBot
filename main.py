import json
import discord
from discord.ext import commands, tasks
import os
from itertools import cycle, islice, chain
import mysql.connector
from database import db
from twitch import TwitchHelix, TwitchClient

with open('credentials.json', 'r') as file:
    credentials = json.load(file)

token = open("token", "r").read()
logChannel = 753963587898310716
twitch = TwitchHelix(client_id=credentials['twitch']['client_id'],
                     oauth_token=credentials['twitch']['oauth_token'])
twitch_client = TwitchClient(client_id=credentials['twitch']['client_id'],
                             oauth_token=credentials['twitch']['oauth_token'])


def get_prefix(client, message):
    try:
        cursor = db.cursor()
        cursor.execute(f'SELECT Prefix FROM Guilds WHERE Guild_ID = {message.guild.id}')
        row = cursor.fetchone()
        return row[0]
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))
        return '!'


client = commands.Bot(command_prefix=get_prefix, case_insensitive=True, description="ScrappyBot")
status = cycle(['!help', 'In Development!', 'Made From Scrap!'])

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.message.add_reaction('❌')
    if isinstance(error, commands.MissingPermissions):
        await ctx.message.add_reaction('❌')


@client.event
async def on_guild_join(guild):
    try:
        cursor = db.cursor()
        cursor.execute(f'INSERT INTO Guilds (Guild_ID, Prefix) VALUES(%s, %s)', (guild.id, "!"))
        db.commit()
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))


@client.event
async def on_guild_remove(guild):
    try:
        cursor = db.cursor()
        cursor.execute(f'DELETE FROM Guilds WHERE Guild_ID = {guild.id}')
        db.commit()
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))


@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online, activity=discord.Game('!help'))
    client.help_command.cog = client.get_cog('General')
    change_status.start()
    twitch_loop.start()
    print('ScrappyBot is online!')
    await client.get_channel(logChannel).send(f'🤖 | {client.user.display_name} is now online!')


@tasks.loop(minutes=5)
async def change_status():
    await client.change_presence(activity=discord.Game(next(status)))


@tasks.loop(minutes=5)
async def twitch_loop():
    print('Twitch loop activated!')
    try:
        cursor = db.cursor()
        cursor.execute(f'SELECT * FROM Twitch')
        row = cursor.fetchall()
        online_channels = []
        channels = []
        for channel in row:
            channels.append(channel[0])
            if channel[2] == 1:
                online_channels.append(channel)
        streams = twitch.get_streams(user_ids=channels)
        for stream in islice(streams, 0, len(streams)):
            if int(stream.user_id) not in chain(*online_channels):
                channel = twitch_client.channels.get_by_id(stream.user_id)
                game = twitch.get_games(game_ids=[stream.game_id])
                for game in islice(game, 0, len(game)):
                    game = game
                embed = discord.Embed(title=stream.title,
                                      description=f'Playing {game.name}',
                                      url=f'https://www.twitch.tv/{stream.user_name}')
                embed.set_author(name=f'{stream.user_name} is live on Twitch!', icon_url=channel.logo,
                                 url=f'https://www.twitch.tv/{stream.user_name}')
                embed.set_thumbnail(url=str(game.box_art_url).replace('-{width}x{height}', ''))
                thumbnail = str(stream.thumbnail_url).replace('-{width}x{height}', '')
                embed.set_image(url=thumbnail)
                cursor.execute(f'SELECT announcement_channel FROM Twitch WHERE channel_id = "{stream.user_id}"')
                row = cursor.fetchall()
                for announcement_channel in row:
                    await client.get_channel(announcement_channel[0]).send(embed=embed)
                try:
                    cursor = db.cursor()
                    cursor.execute(f'UPDATE Twitch SET online = "1" WHERE channel_id = {stream.user_id}')
                    db.commit()
                except mysql.connector.Error as err:
                    print("Something went wrong: {}".format(err))

        for channel in online_channels:
            stream = twitch_client.streams.get_stream_by_user(channel_id=channel[0])
            if not stream:
                twitch_channel = twitch_client.channels.get_by_id(channel_id=channel[0])
                try:
                    cursor = db.cursor()
                    cursor.execute(f'UPDATE Twitch SET online = "0" WHERE channel_id = {twitch_channel.id}')
                    db.commit()
                except mysql.connector.Error as err:
                    print("Something went wrong: {}".format(err))
                embed = discord.Embed(title=f'{twitch_channel.display_name} has stopped streaming...')
                await client.get_channel(channel[1]).send(embed=embed)

    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))


client.run(token)
