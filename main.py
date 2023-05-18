import discord
from discord.ext import commands
from discord.ui import Button, View

import os
from dotenv import load_dotenv

from quiz import Quiz
from joker import tell_joke
from error import AlreadyDoneError, GameStartedError, NoGameError

# Init
intents = discord.Intents.all()
help_command = commands.DefaultHelpCommand(no_category = 'Quizy')
bot = commands.Bot(command_prefix='?', intents = intents, help_command=help_command)

# Variables
quiz: Quiz = None

# Commands
@bot.command(name="play", brief='Create or join the game', description='Create a new Quizy game or add the player to the existing one')
async def play_command(ctx: commands.Context):
    try:
        player_num = play(str(ctx.message.author.id))

        if player_num == 1:
            view = View()

            join_button = Button(label="Join", style=discord.ButtonStyle.primary, emoji="🤩")
            async def join_button_callback(interact: discord.Interaction):
                try:
                    play(str(interact.user.id))
                    return await interact.response.send_message(f'☺ Welcome to the game {interact.user.mention}')
                except Exception as e:
                    return await interact.response.send_message(str(e))
            join_button.callback = join_button_callback
            view.add_item(join_button)

            return await ctx.send(f'😱 {ctx.message.author.mention} started a new Quizy game. Call your friends and tell them to join', view= view)
        else:
            return await ctx.send(f'☺ Welcome to the game {ctx.message.author.mention}')
    except Exception as e:
        return await ctx.send(str(e))

@bot.command(name="start", brief='Start match', description='Begin the match to start answering the questions of the trivia game')
async def start_command(ctx: commands.Context, rounds:int= commands.parameter(default=2, description='The number of rounds')):    
    try:
        start(rounds)
    except Exception as e:
        return await ctx.send(str(e))
    
    await show_question(ctx.channel)

@bot.command(name="end", brief='End the current game', description='Finish the current Quizy game and display the partial results')
async def end_command(ctx: commands.Context):
    global quiz

    scores = quiz.scores()
    await ctx.send("**Results:**\n"+'\n'.join([f"**{(await bot.fetch_user(player)).mention}:** {scores[player]}" for player in scores]))
    quiz = None

    await ctx.send("Game ended 😞")

@bot.command(name="info", brief='Display game information', description='Display game information')
async def info_command(ctx: commands.Context):
    global quiz

    information = "Quiz not yet created 😬"
    if quiz:
        information = str(quiz)

    await ctx.send(information)

@bot.command(name="joke", brief='Tell a joke', description='Generate a funny and eloquent joke from a variety of topics')
async def joke_command(ctx: commands.Context):
    await ctx.send("Let me think... 🤔")
    await ctx.send(tell_joke())

#NPI
async def show_question(channel: discord.channel.TextChannel):
    global quiz

    actual_question = quiz.actual_question()
    user = await bot.fetch_user(actual_question.player)

    view: View = View()

    a_button = Button(label="A", style=discord.ButtonStyle.secondary)
    b_button = Button(label="B", style=discord.ButtonStyle.secondary)
    c_button = Button(label="C", style=discord.ButtonStyle.secondary)
    d_button = Button(label="D", style=discord.ButtonStyle.secondary)

    async def answer_callback(interact: discord.Interaction, answer: str):# Check "This interaction failed"
        global quiz
        
        quiz.answer_question(str(interact.user.id), answer)
        
        if actual_question != quiz.actual_question():
            await message.delete()
            if not quiz.ended:
                await show_question(interact.channel)
            else:
                scores = quiz.scores()
                await interact.response.send_message("**Results:**\n"+'\n'.join([f"**{(await bot.fetch_user(player)).mention}:** {scores[player]}" for player in scores]))
                quiz = None
        
        await interact.response.defer()

    a_button.callback = lambda interact: (await answer_callback(interact, answer="B") for _ in '_').__anext__()
    view.add_item(a_button)

    b_button.callback = lambda interact: (await answer_callback(interact, answer="B") for _ in '_').__anext__()
    view.add_item(b_button)

    c_button.callback = lambda interact: (await answer_callback(interact, answer="C") for _ in '_').__anext__()
    view.add_item(c_button)

    d_button.callback = lambda interact: (await answer_callback(interact, answer="D") for _ in '_').__anext__()
    view.add_item(d_button)

    message = await channel.send(f"What would **{user.mention}** say:\n{actual_question.question}", view=view)

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

def start(rounds: int):
    global quiz

    if quiz:
        inited = quiz.init_match(rounds)
        if not inited:
            if quiz.started:
                raise GameStartedError
            elif len(quiz.players) < 2:
                raise ValueError("There are not enough players (at least 2)")
            else:
                raise ValueError("Invalid number of rounds (must be a positive integer)")
    else:
        raise NoGameError

async def info() -> str:
    global quiz

    information = "**Quizy**\n\n"

    if quiz:
        players = [await bot.fetch_user(player_id) for player_id in quiz.players]
        information += f'**players**:{", ".join([p.mention for p in players])}'
    else:
        raise NoGameError

    return information



load_dotenv()
bot.run(os.getenv("DISCORD_API_KEY"))