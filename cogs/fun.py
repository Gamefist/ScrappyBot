import html
import aiohttp
import discord
from discord.ext import commands
import random

class Fun(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Fun Cog Loaded Successfully!')

    @commands.command(name="Trivia", help="Get a true or false question about videogames")
    async def trivia(self, ctx):
        async with ctx.channel.typing():
            async with aiohttp.ClientSession() as session:
                async with session.get(
                        f'https://opentdb.com/api.php?amount=1&category=15&difficulty=medium&type=boolean') as request:
                    data = await request.json()
                    question = html.unescape(data["results"][0]["question"])
                    answer = data["results"][0]["correct_answer"]
                    embed = discord.Embed(title=f'Trivia with: **{ctx.message.author.display_name}**')
                    embed.add_field(name=f'Your question:', value=question, inline=False)
                    embed.set_footer(text='Trivia by Sparky', icon_url=self.client.user.avatar_url)
                    embed.set_thumbnail(url=ctx.message.author.avatar_url)
                    message = await ctx.send(embed=embed)
                    await message.add_reaction('✅')
                    await message.add_reaction('❌')

                    def check(reaction, user):
                        return user == ctx.message.author and str(reaction.emoji) in ['❌', '✅']

                    reacted, user_reacted = await self.client.wait_for('reaction_add', check=check)
                    if str(reacted.emoji) == '✅':
                        if answer == "True":
                            embed.add_field(name=f'Your answer is:', value="Correct!!", inline=False)
                            await message.edit(embed=embed)
                            await message.clear_reactions()
                        else:
                            embed.add_field(name=f'Your answer is:', value="Wrong..", inline=False)
                            await message.edit(embed=embed)
                            await message.clear_reactions()
                    elif str(reacted.emoji) == '❌':
                        if answer == "False":
                            embed.add_field(name=f'Your answer is:', value="Correct!!", inline=False)
                            await message.edit(embed=embed)
                            await message.clear_reactions()
                        else:
                            embed.add_field(name=f'Your answer is:', value="Wrong..", inline=False)
                            await message.edit(embed=embed)
                            await message.clear_reactions()

    @commands.command(name="8ball", help="A Magic 8Ball!")
    async def _8ball(self, ctx, *, question):
        answers = ['It is certain', 'It is decidedly so', 'Without a doubt', 'Yes – definitely', 'You may rely on it',
                   'As I see it, yes', 'Most likely', 'Outlook good', 'Yes Signs point to yes', 'Reply hazy',
                   'try again',
                   'Ask again later', 'Better not tell you now', 'Cannot predict now', 'Concentrate and ask again',
                   'Dont count on it', 'My reply is no', 'My sources say no', 'Outlook not so good', 'Very doubtful']
        embed = discord.Embed(title='🎱 | Magic 8ball!')
        embed.add_field(name='Question:', value=f'{question}', inline=False)
        embed.add_field(name='Answer:', value=f'{random.choice(answers)}', inline=False)
        await ctx.send(embed=embed)

    @_8ball.error
    async def _8ball_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f'{ctx.message.author.mention} Please specify a question for the magic 8ball!')


def setup(client):
    client.add_cog(Fun(client))
