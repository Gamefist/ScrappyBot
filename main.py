import discord
from discord.ext import commands, tasks
import os
from itertools import cycle
import json

token = open("token", "r").read()


def get_prefix(client, message):
    with open('./prefixes.json', 'r') as file:
        prefixes = json.load(file)

    return prefixes[str(message.guild.id)]


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
    with open('./prefixes.json', 'r') as file:
        prefixes = json.load(file)

    prefixes[str(guild.id)] = '!'

    with open('./prefixes.json', 'w') as file:
        json.dump(prefixes, file, indent=4)


@client.event
async def on_guild_remove(guild):
    with open('./prefixes.json', 'r') as file:
        prefixes = json.load(file)

    prefixes.pop(str(guild.id))

    with open('./prefixes.json', 'w') as file:
        json.dump(prefixes, file, indent=4)


@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online, activity=discord.Game('!help'))
    client.help_command.cog = client.get_cog('General')
    change_status.start()
    print('ScrappyBot is online!')


@tasks.loop(minutes=5)
async def change_status():
    await client.change_presence(activity=discord.Game(next(status)))


client.run(token)
