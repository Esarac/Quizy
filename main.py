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

# Events
@bot.event
async def on_reaction_add(reaction, user):
    print(reaction.message)
    await user.send("Hello")

# Commands
@bot.command()
async def play(ctx):
    global quiz

    if quiz and quiz.started():
        return await ctx.send("Sorry, but the match have already started 😅")
    
    message: str = ""
    if not quiz:
        quiz = Quiz(ctx.message.author.name)
        message = f'{ctx.message.author.mention} started a new Quizy game. Call your friends and tell them to join 🤩'
    else:
        added:bool = quiz.register_player(ctx.message.author.name)
        message = f'Welcome to the game {ctx.message.author.mention} ☺.' if added else "You are all ready playing 🙄"
    
    await ctx.send(message)

@bot.command()
async def start(ctx, rounds:int=2):
    global quiz

    inited = quiz.init_match(3)

    if not inited:
        if quiz.started():
            await ctx.send("The match have already started 😅")
        else:
            await ctx.send("Sorry, but theres not enough players to start (at least 2) 😫")
        return
    
    await ctx.send("Let the play begin! 🤭")
    first_question = quiz.pop_question()
    await ctx.send(f"What would **{first_question[0]}** say:\n{first_question[1]}")

@bot.command()
async def end(ctx):
    global quiz

    quiz = None
    await ctx.send("Game ended 😞")

@bot.command()
async def info(ctx):
    global quiz

    information = "Quiz not yet created 😬"
    if quiz:
        information = str(quiz)

    await ctx.send(information)

@bot.command()
async def joke(ctx):
    await ctx.send("Let me think... 🤔")
    await ctx.send(tell_joke())

load_dotenv()
bot.run(os.getenv("DISCORD_API_KEY"))
