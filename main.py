import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from quiz import Quiz
from joker import tell_joke

# Init
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='?', intents = intents)

# Variables
quiz: Quiz = None

# Commands
@bot.command()
async def play(ctx):
    global quiz

    if quiz and quiz.started:
        return await ctx.send("Sorry, but the match have already started 😅")
    
    message: str = ""
    if not quiz:
        quiz = Quiz(ctx.message.author.name, 2)
        message = f'{ctx.message.author.mention} started a new Quizy game. Call your friends and tell them to join 🤩'
    else:
        added:bool = quiz.register_player(ctx.message.author.name)
        message = f'Welcome to the game {ctx.message.author.mention} ☺.' if added else "You are all ready playing 🙄"
    
    await ctx.send(message)

@bot.command()
async def start(ctx):
    global quiz

    quiz.started = True
    await ctx.send("Let the play begin! 🤭")

@bot.command()
async def end(ctx):
    global quiz

    quiz = None
    await ctx.send("Game ended 😞")

@bot.command()
async def info(ctx):
    global quiz

    if not quiz:
        information = "Quiz not yet created 😬"
    else:
        information =f"""**Players:** {", ".join(quiz.players)}
**Rounds:** {str(quiz.rounds)}
"""
        if quiz.started:
            information += f"**Started**"

    await ctx.send(information)

@bot.command()
async def joke(ctx):
    await ctx.send(tell_joke())

load_dotenv()
bot.run(os.getenv("DISCORD_API_KEY"))
