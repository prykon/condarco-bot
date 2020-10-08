# bot.py
import os, random, requests

import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')


client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')
    for guild in client.guilds:
        if guild.name == GUILD:
            break

    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )


@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hola {member.name}, te damos la bienvenida al servidor de Discord del grupo de jóvenes de Condarco!'
    )


@client.event
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

client.run(TOKEN)