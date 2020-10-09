import discord
from discord.ext import commands, tasks
import os
from itertools import cycle
import mysql.connector
from database import db

token = open("token", "r").read()
logChannel = 753963587898310716


def get_prefix(client, message):
    try:
        cursor = db.cursor()
        cursor.execute(f'SELECT Prefix FROM Guilds WHERE Guild_ID = {message.guild.id}')
        row = cursor.fetchone()
        return row[0]
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))


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
    print('ScrappyBot is online!')
    await client.get_channel(logChannel).send(f'🤖 | {client.user.display_name} is now online!')


@tasks.loop(minutes=5)
async def change_status():
    await client.change_presence(activity=discord.Game(next(status)))


client.run(token)
