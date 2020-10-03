import random

from discord.ext import commands


class Fun(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Fun Cog Loaded Successfully!')

    @commands.command(name="8ball", help="A Magic 8Ball!")
    async def _8ball(self, ctx, *, question):
        answers = ['It is certain', 'It is decidedly so', 'Without a doubt', 'Yes – definitely', 'You may rely on it',
                   'As I see it, yes', 'Most likely', 'Outlook good', 'Yes Signs point to yes', 'Reply hazy',
                   'try again',
                   'Ask again later', 'Better not tell you now', 'Cannot predict now', 'Concentrate and ask again',
                   'Dont count on it', 'My reply is no', 'My sources say no', 'Outlook not so good', 'Very doubtful']
        await ctx.send(f'Question: {question}\nAnswer: {random.choice(answers)}')


def setup(client):
    client.add_cog(Fun(client))
