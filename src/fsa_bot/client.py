import discord

from dotenv import load_dotenv

import fsa_bot.lib as lib


load_dotenv()
client = discord.Client()
logger = lib.logger


@client.event
async def on_ready():
    logger.info(f'Logged in as {client.user}')


@client.event
async def on_message(message: discord.message.Message):
    if message.author == client.user:
        return


if __name__ == '__main__':  # pragma: no cover
    client.run()
