from os import name
import discord
import logging
import json

# Bot Token
token = 'Insert your token here'

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
about = discord.Embed()
about.title = 'PoliResourceBot'
about.description = 'Bot creato da Mario Merlo usando la libreria discord.py ~~e tanta documentazione~~'
about.set_thumbnail(url='https://i.ibb.co/BLTq2mH/icon.png')
about.add_field(name='Il mio canale', value='[YouTube](https://www.youtube.com/watch?v=dQw4w9WgXcQ)', inline=False)
about.add_field(name='Seguitemi su GitHub', value='[Clicca qui](https://www.github.com/MrVideo)', inline=False)
about.add_field(name='Repository di GitHub', value='[Clicca qui](https://www.github.com/MrVideo/PoliResourceBot)', inline=False)

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

# Create new client
client = discord.Client()

# When the login is successful, this message gets shown on the console
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

# When these messages are sent
@client.event
async def on_message(message):

    global resourceDict
    reloadStr = '$reload'
    aboutStr = '$about'
    helpStr = '$help'

    # If the bot itself sent a message it gets ignored
    if message.author == client.user:
        return
    
    # Resource message
    if message.content.startswith('$res'):
        # Splits the message into command and resource index
        array = message.content.split(' ')
        if array[1].isdecimal():
            try:
                # Tries to fetch the correct resource
                await message.channel.send('Ecco la risorsa che cercavi: ' + resourceDict[int(array[1])]['url'])
            except IndexError:
                # Catches IndexError exception if the resource is outside of array boundaries
                await message.channel.send('Mi dispiace, la risorsa non esiste. Riprova')
        elif array[1] == 'list':
            index = 0
            for entry in resourceDict:
                list.add_field(name='Risorsa ' + str(index), value=entry['name'], inline=False)
                index = index + 1
            await message.channel.send('Ecco una lista delle risorse disponibili', embed=list)
            list.clear_fields()

    # Reload message
    elif message.content == reloadStr:
        # Re-opens and re-loads the JSON file
        f = open('resources.json')
        resourceDict = json.load(f)
        f.close()
        await message.channel.send('Le risorse sono state ricaricate!')
    
    # About message
    elif message.content == aboutStr:
        await message.channel.send(embed=about)

    elif message.content == helpStr:
        await message.channel.send(embed=helpEmbed)

# The client is run
client.run(token)
