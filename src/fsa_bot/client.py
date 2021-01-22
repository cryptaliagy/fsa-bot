import discord
from discord.ext import commands
import os

from dotenv import load_dotenv

import fsa_bot.lib as lib

import pyfsa.lib.fsa as fsa
import pyfsa.lib.csv_convert as csv


load_dotenv()
intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(
    command_prefix='$',
    description='''
    A bot to render state diagrams from inline csv.
    Check out http://tlia.ca/fsa-bot for info on the
    bot, and http://tlia.ca/fsa for the engine
    that powers it
    ''',
    intents=intents
)
logger = lib.logger


@bot.event
async def on_ready():
    logger.info(f'Logged in as {bot.user.name}')


@bot.command
async def state(ctx, csv_str: str, *args: str):
    trans_dicts = lib.csv_string_to_dicts(csv_str)
    transitions = csv.rows_to_transitions(trans_dicts)

    fsa.get_state_graph(
        transitions
    )

    ctx.send(file='output.png')

if __name__ == '__main__':  # pragma: no cover
    bot.run(os.environ['DISCORD_TOKEN'])
