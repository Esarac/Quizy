import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from quiz import Quiz

# Init
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents = intents)

# Variables
quiz: Quiz = None

# Commands
@bot.command()
async def register(ctx):
    global quiz
    message: str = "NaN"

    if not quiz:
        quiz = Quiz(ctx.message.author.name)
        message = f'{ctx.message.author.mention} started a new Quizy game. Call your friends and tell them to join <3.'
    else:
        added:bool = quiz.register_player(ctx.message.author.name)
        message = f'Welcome to the game {ctx.message.author.mention}.' if added else "You are all ready registered."
    
    await ctx.send(message)


load_dotenv()
bot.run(os.getenv("DISCORD_API_KEY"))
 
# @bot.command()
# async def new(ctx, arg):
#     
#     await ctx.send(arg)

# @bot.command()
# async def start(ctx, arg):
#     await ctx.send(quiz)

# @bot.command()
# async def play(ctx, arg):
#     await ctx.author.send(str(quiz.output))

# @bot.command(list='foo')
# async def foo(ctx, arg):
#     await ctx.send(arg)
