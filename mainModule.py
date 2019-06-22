from discord.ext.commands import Bot
from discord.utils import get
import json
import os
import asyncio
import datetime
import discord

BOT_PREFIX =('.')
TOKEN = 'NTM5NTQ3MzA4MTI4MzM3OTMw.DzD-Wg.0NgHbnUWb0mQQJnwDFIltwzSbUI'

client = Bot(command_prefix=BOT_PREFIX)

extensions = ['gatherable', 'inventory', 'give_craft']

@client.command()
async def load(extension):
    try:
        client.load_extension(extension)
        print('Loaded {}'.format(extension))
    except Exception as error:
        print('{} cannot be loaded. [{}]'.format(extension, error) )

@client.command()
async def unload(extension):
    try:
        client.unload_extension(extension)
        print('Unloaded {}'.format(extension))
    except Exception as error:
        print('{} cannot be unloaded. [{}]'.format(extension, error))


if __name__ == '__main__':
    for extension in extensions:
        try:
            client.load_extension(extension)
            print('Loaded {}'.format(extension))
        except Exception as error:
            print('{} cannot be loaded. [{}]'.format(extension, error))


client.run(TOKEN)