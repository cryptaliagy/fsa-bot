# -*- coding: utf-8 -*-
import discord  # type: ignore
from discord.ext import commands  # type: ignore
import os

from dotenv import load_dotenv
from typing import Dict

import fsa_bot.lib as lib

import pyfsa.lib.fsa as fsa
import pyfsa.lib.csv_convert as csv


load_dotenv()
intents = discord.Intents()
intents.guild_messages = True

bot = commands.Bot(
    command_prefix='$',
    description='''
    A bot to render state diagrams from inline csv.
    Check out http://tlia.ca/fsa-bot for info on the
    bot, and http://tlia.ca/fsa for the engine
    that powers it
    ''',
    help_command=None,
    intents=intents
)
logger = lib.logger


@bot.event
async def on_ready():
    logger.info(f'Logged in as {bot.user.name}')


@bot.event
async def on_command_error(ctx, error):
    logger.critical(error)

    ctx.send(error)


@bot.command()
async def state(ctx, csv_str: str, *args: str):
    valid_args = [
        'start',
        'end',
        'engine'
    ]
    trans_dicts = lib.csv_string_to_dicts(csv_str)
    transitions = csv.rows_to_transitions(trans_dicts)

    arg_keys = lib.keyval_to_dict(*args)

    passthrough: Dict[str, str] = {}

    for arg in valid_args:
        if arg in arg_keys:
            passthrough[arg] = arg_keys[arg]

    fsa.get_state_graph(
        transitions,
        **passthrough  # type: ignore
    )

    logger.info(transitions)

    with open('output.png', 'rb') as f:
        fp = discord.File(f)
        await ctx.send(file=fp)


# Disabled while PyFSA does not allow use of the `string` command
# @bot.command()
async def string(ctx, *args: str):
    required_args = [
        'start',
        'end',
        'string'
    ]
    valid_args = [
        *required_args,
        'engine',
    ]
    arg_keys = lib.keyval_to_dict(*args)
    states = arg_keys.get('states', '')

    trans_dicts = lib.csv_string_to_dicts(states)
    transitions = csv.rows_to_transitions(trans_dicts)

    passthrough: Dict[str, str] = {}

    for arg in valid_args:
        if arg in arg_keys:
            passthrough[arg] = arg_keys[arg]

    for arg in required_args:
        if arg not in passthrough:
            await ctx.send(
                f'Missing required argument "{arg}"'
            )
            return

    try:
        fsa.render_string_graph(
            transitions=transitions,
            **passthrough  # type: ignore
        )
    except Exception as e:
        logger.critical(e)
        await ctx.send(
            'Unable to render the graph, '
            'reach out to Natalia at '
            'vellista#3040 to see what went '
            'wrong.'
        )
        return
    logger.info(transitions)
    logger.info(passthrough)

    with open('output.png', 'rb') as f:
        fp = discord.File(f)
        await ctx.send(file=fp)


@bot.command()
async def help(ctx, *_: str):
    await ctx.send(
        '''
Welcome to the finite state automata bot!

Check out the readme for this project at
http://tlia.ca/fsa-bot which will go
through examples and uses of this bot.

This bot uses the PyFSA library as a backend,
so you can find more information on
http://tlia.ca/fsa
        '''
    )


def main():
    bot.run(os.environ['DISCORD_TOKEN'])


if __name__ == '__main__':  # pragma: no cover
    main()
