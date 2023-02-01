import discord
from discord.ext import commands
from discord.ui import Button, View

import os
from dotenv import load_dotenv

from quiz import Quiz
from joker import tell_joke
from error import AlreadyDoneError, GameStartedError

# Init
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='?', intents = intents)

# Variables
quiz: Quiz = None

# Commands
@bot.command(name="play")
async def play_command(ctx: commands.Context):
    try:
        player_num = play(str(ctx.message.author.id))

        if player_num == 1:
            view = View()

            join_button = Button(label="Join", style=discord.ButtonStyle.primary, emoji="🤩")
            async def join_button_callback(interact: discord.Interaction):
                try:
                    play(str(interact.user.id))
                    return await interact.response.send_message(f'☺ Welcome to the game {ctx.message.author.mention}')
                except Exception as e:
                    return await interact.response.send_message(str(e))
            join_button.callback = join_button_callback
            view.add_item(join_button)

            return await ctx.send(f'😱 {ctx.message.author.mention} started a new Quizy game. Call your friends and tell them to join', view= view)
        else:
            return await ctx.send(f'☺ Welcome to the game {ctx.message.author.mention}')
    except Exception as e:
        return await ctx.send(str(e))

@bot.command(name="start")
async def start_command(ctx: commands.Context, rounds:int=2):
    global quiz

    inited = quiz.init_match(rounds)

    if not inited:
        if quiz.started():
            await ctx.send("😅 The match have already started")
        else:
            await ctx.send("😫 Sorry, but theres not enough players to start (at least 2)")
        return
    
    await show_question(ctx.channel)

@bot.command()
async def end(ctx: commands.Context):
    global quiz

    quiz = None
    await ctx.send("Game ended 😞")

@bot.command()
async def info(ctx: commands.Context):
    global quiz

    information = "Quiz not yet created 😬"
    if quiz:
        information = str(quiz)

    await ctx.send(information)

@bot.command()
async def joke(ctx: commands.Context):
    await ctx.send("Let me think... 🤔")
    await ctx.send(tell_joke())

# Services
def play(player_id: str) -> int:
    global quiz
    
    player_index: int = 0

    if not quiz:
        quiz = Quiz(player_id)
        player_index = 1
    else:
        if not quiz.started:
            added:bool = quiz.register_player(player_id)
            player_index = len(quiz.players)
            if not added:
                raise AlreadyDoneError
        else:
            raise GameStartedError
    
    return player_index

async def show_question(channel: discord.channel.TextChannel):
    global quiz

    actual_question = quiz.actual_question()
    user = await bot.fetch_user(actual_question.player)

    view: View = View()

    a_button = Button(label="A", style=discord.ButtonStyle.secondary)
    b_button = Button(label="B", style=discord.ButtonStyle.secondary)
    c_button = Button(label="C", style=discord.ButtonStyle.secondary)
    d_button = Button(label="D", style=discord.ButtonStyle.secondary)

    async def answer_callback(player: str, answer: str):# Check "This interaction failed"
        global quiz
        
        quiz.answer_question(player, answer)
        
        if actual_question != quiz.actual_question():
            await message.delete()
            if not quiz.ended:
                await show_question(channel)
            else:
                scores = quiz.scores()
                await channel.send("**Results:**\n"+'\n'.join([f"**{(await bot.fetch_user(player)).mention}:** {scores[player]}" for player in scores]))
                quiz = None
    
    a_button.callback = lambda interact: (await answer_callback(str(interact.user.id), answer="A") for _ in '_').__anext__()
    view.add_item(a_button)

    b_button.callback = lambda interact: (await answer_callback(str(interact.user.id), answer="B") for _ in '_').__anext__()
    view.add_item(b_button)

    c_button.callback = lambda interact: (await answer_callback(str(interact.user.id), answer="C") for _ in '_').__anext__()
    view.add_item(c_button)

    d_button.callback = lambda interact: (await answer_callback(str(interact.user.id), answer="D") for _ in '_').__anext__()
    view.add_item(d_button)

    message = await channel.send(f"What would **{user.mention}** say:\n{actual_question.question}", view=view)

load_dotenv()
bot.run(os.getenv("DISCORD_API_KEY"))