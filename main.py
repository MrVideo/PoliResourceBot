import discord
from discord.ext import commands
import logging
import json

from discord.ext.commands.errors import CommandNotFound, MissingRequiredArgument, TooManyArguments
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

# Open JSON array for Webex links
w = open('webex.json')
webexDict = json.load(w)
w.close()

# Create "About" embed
aboutEmbed = discord.Embed()
aboutEmbed.title = 'PoliResourceBot'
aboutEmbed.description = 'Bot creato da Mario Merlo usando la libreria discord.py ~~e tanta documentazione~~'
aboutEmbed.set_thumbnail(url='https://i.ibb.co/BLTq2mH/icon.png')
aboutEmbed.add_field(name='Repository di GitHub', value='[Clicca qui](https://www.github.com/MrVideo/PoliResourceBot)', inline=False)
aboutEmbed.add_field(name="Documentazione Bot", value="[Clicca qui](https://mariomerlo.me/poli)", inline=False)
aboutEmbed.add_field(name='Il mio sito', value="[Clicca qui](https://mariomerlo.me)", inline=False)
aboutEmbed.add_field(name='Il mio canale', value='[YouTube](https://www.youtube.com/watch?v=dQw4w9WgXcQ)', inline=False)

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
helpEmbed.add_field(name='Cerca link aule virtuali', value='``$webex <prof/subj> <nome>``', inline=False)

# Create "Webex" embed
webexEmbed = discord.Embed()
webexEmbed.title = 'Risultati di ricerca'
webexEmbed.description = 'Non è stato trovato alcun professore con questi criteri di ricerca'

# Create selected resource embed
resEmbed = discord.Embed()
resEmbed.title = "Ecco la risorsa richiesta"
resEmbed.description = "Usa il comando ``$res <ID>`` per recuperare altre risorse."

# Removes default help command
client.remove_command('help')

@client.event
# When the login is successful, this message gets shown on the console
async def on_ready():
    await client.change_presence(activity=discord.Game(name='scrivi $help'))
    print('We have logged in as {0.user}'.format(client))

@client.event
# Command listener
async def on_message(message):
    if message.content.startswith('$'):
        await client.process_commands(message)
# Error handler
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        await ctx.send("Mi dispiace, ma quel comando non esiste.")
    elif isinstance(error, MissingRequiredArgument):
        await ctx.send("Mi dispiace, ma mancano degli argomenti necessari. Riprova!")
    elif isinstance(error, TooManyArguments):
        await ctx.send("Mi dispiace, ma hai messo troppi argomenti. Prova a toglierne qualcuno!")
    else:
        raise error

# Commands
@client.command()
async def reload(ctx):
    "Reloads resources"
    f = open('resources.json')
    w = open('webex.json')
    global resourceDict
    global webexDict
    resourceDict = json.load(f)
    webexDict = json.load(w)
    f.close()
    w.close()
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
            resEmbed.add_field(name=resourceDict[int(arg)]['name'], value=resourceDict[int(arg)]['url'])
            await ctx.send(embed=resEmbed)
        except IndexError:
            await ctx.send("Mi dispiace, ma quella risorsa non esiste.")
        finally:
            resEmbed.clear_fields()
    elif arg == 'list':
        i = 0
        for entry in resourceDict:
            list.add_field(name='Risorsa ' + str(i), value=entry['name'], inline=False)
            i += 1
        await ctx.send('Ecco una lista delle risorse disponibili', embed=list)
        list.clear_fields()
    else:
        await ctx.send("Mi dispiace ma hai inserito dei caratteri non validi.")

@client.command()
async def webex(ctx, type: str, arg: str):
    "Sends information about professors and their virtual classroom link"
    if type == 'prof':
        for entry in webexDict:
            if arg.lower() in entry['prof'].lower():
                webexEmbed.add_field(name=entry['prof'] + ' - ' + entry['subject'], value='http://politecnicomilano.webex.com/meet/' + entry['link'], inline=False)
                webexEmbed.description = 'Ecco i risultati per la tua ricerca'
        await ctx.send('Ecco cos\'ho trovato: ', embed=webexEmbed)
    elif type == 'subj':
        for entry in webexDict:
            if arg.lower() in entry['subject'].lower():
                webexEmbed.add_field(name=entry['prof'] + ' - ' + entry['subject'], value='http://politecnicomilano.webex.com/meet/' + entry['link'], inline=False)
                webexEmbed.description = 'Ecco i risultati per la tua ricerca'
        await ctx.send('Ecco cos\'ho trovato: ', embed=webexEmbed)   
    else:
        await ctx.send('Hai inserito un tipo non valido. Riprova.')
    webexEmbed.description = 'Non è stato trovato alcun professore con questi criteri di ricerca'
    webexEmbed.clear_fields()

# Does not ignore too many arguments on one command
for command in client.commands:
    command.ignore_extra = False

# The client is run
client.run(token)
