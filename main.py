from os import name
import discord
from discord.ext import commands
import logging
import json
from private.config import token

# Create new client
intents = discord.Intents.default()
description = 'A bot that serves university resources'
client = commands.Bot(command_prefix='$', intents=intents, description=description)

# Logger code
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

# Open JSON array for resources
f = open('resources.json')
resourceDict = json.load(f)
f.close()

# Create "About" embed
aboutEmbed = discord.Embed()
aboutEmbed.title = 'PoliResourceBot'
aboutEmbed.description = 'Bot creato da Mario Merlo usando la libreria discord.py ~~e tanta documentazione~~'
aboutEmbed.set_thumbnail(url='https://i.ibb.co/BLTq2mH/icon.png')
aboutEmbed.add_field(name='Il mio canale', value='[YouTube](https://www.youtube.com/watch?v=dQw4w9WgXcQ)', inline=False)
aboutEmbed.add_field(name='Seguitemi su GitHub', value='[Clicca qui](https://www.github.com/MrVideo)', inline=False)
aboutEmbed.add_field(name='Repository di GitHub', value='[Clicca qui](https://www.github.com/MrVideo/PoliResourceBot)', inline=False)

# Create "Resource List" embed
list = discord.Embed()
list.title = 'Lista delle risorse disponibili'
list.description = 'Seleziona una delle risorse con il comando ``$res <ID>``'
list.clear_fields()

# Create "Help" embed
helpEmbed = discord.Embed()
helpEmbed.title = 'Lista dei comandi disponibili'
helpEmbed.description = 'Il prefisso del bot è ``$``'
helpEmbed.set_thumbnail(url='https://i.ibb.co/hVXnBCs/helpicon.png')
helpEmbed.add_field(name='Aiuto', value='``$help``', inline=False)
helpEmbed.add_field(name='Lista risorse', value='``$res list``', inline=False)
helpEmbed.add_field(name='Richiedi risorsa', value='``$res <ID>``', inline=False)
helpEmbed.add_field(name='Informazioni sul bot', value='``$about``', inline=False)
helpEmbed.add_field(name='Ricarica lista risorse', value='``$reload``', inline=False)

# Removes default help command
client.remove_command('help')

@client.event
# When the login is successful, this message gets shown on the console
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
# Command listener
async def on_message(message):
    if message.startswith('$'):
        await client.process_commands(message)

# Commands
@client.command()
async def reload(ctx):
    "Reloads resources"
    f = open('resources.json')
    global resourceDict
    resourceDict = json.load(f)
    f.close()
    await ctx.send('Le risorse sono state ricaricate.')

@client.command()
async def about(ctx):
    "Sends an embed with about information"
    await ctx.send(embed=aboutEmbed)

@client.command()
async def help(ctx):
    "Sends a help table"
    await ctx.send(embed=helpEmbed)

@client.command()
async def res(ctx, arg: str):
    "Sends a selected resource or the list of resources"
    if arg.isdecimal():
        try:
            await ctx.send("Ecco la risorsa che cercavi: " + resourceDict[int(arg)]['url'])
        except IndexError:
            await ctx.send("Mi dispiace, ma quella risorsa non esiste.")
    elif arg == 'list':
        i = 0
        for entry in resourceDict:
            list.add_field(name='Risorsa ' + str(i), value=entry['name'], inline=False)
            i += 1
        await ctx.send('Ecco una lista delle risorse disponibili', embed=list)
        list.clear_fields()

# The client is run
client.run(token)
