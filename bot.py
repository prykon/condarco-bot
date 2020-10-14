# bot.py
import os, random, requests
import logging

import discord
from discord.ext import commands

from dotenv import load_dotenv

import json
import itertools

# setup logging
logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename='discord.log', mode='w', encoding='utf-8')
handler.setFormatter(logging.Formatter('%(asctime)s : %(levelname)s : %(name)s > %(message)s'))
logger.addHandler(handler)

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = commands.Bot(command_prefix='..', case_insensitive=True)


@client.event
async def on_ready():
    logger.info(f'{client.user.name} has connected to Discord!')

    guild = discord.utils.get(client.guilds, id=int(GUILD))

    if guild is None:
        logger.warning(f'Could not find the expected guild for {client.user}')
        return

    logger.info(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name} (id: {guild.id})'
    )


@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hola {member.name}, te damos la bienvenida al servidor de Discord del grupo de jóvenes de Condarco!'
    )


# @client.event
async def on_message(message):
    if message.author == client.user:
        return

    bendiciones = [
        'Amen!',
        'Predícalo!',
    ]

    if message.content == 'Dios es bueno':
        response = random.choice(bendiciones)
        await message.channel.send(response)


    orando = ['Uh, vamos a estar orando...', 'Qué garrón. Oramos...', 'Llevemos unos las cargas de los otros... oramos.']
    orando_triggers = ['enfermo', 'enferma', 'en cama', 'internado', 'internada', 'está en el hospital']
    if any(ot in message.content for ot in orando_triggers):
        response = random.choice(orando)
        await message.channel.send(response)


@client.command()
async def versiculo(context, libro, capitulo, inicio, fin, version='RVR1960'):
    the_one_true_versicle = '```Porque de tal manera amo Dios al mundo que ha dado a su hijo unigénito, ' \
                            'para que todo aquel que en él cree no se pierda, mas tenga vida eterna.```'

    url = 'http://getbible.net/json'
    search = f'{libro} {capitulo}:{inicio}-{fin}'
    r = requests.get(url=url, params={'passage': search, 'version': version})

    data = dict(json.loads(r.text[1:-2]))
    logger.info(f"la daata {data['book'][0]['chapter'].values()}")
    xs = [ch['verse'] for ch in data['book'][0]['chapter'].values()]

    verses = ''
    for v in xs:
        verses += v

    await context.send(verses)


client.run(TOKEN)