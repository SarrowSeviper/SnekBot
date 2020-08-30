import asyncio
import discord
import json
import os
import random
from modules import Fun
from utils import DatabaseController

client = discord.Client()

prefix = "$"
dirPath = os.path.dirname(os.path.abspath(__file__))
confPath = dirPath + '\\config.json'
dbPath = dirPath + '\\snekbot.db'
config = json.load(open(confPath))
token = config['token']
owner_id = config['owner_id']
db = DatabaseController
conn = db.create_connection(dbPath)
busy = False


@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=prefix+'help'))
    print('{0.user} is now running.'.format(client))
    channel = client.get_channel(744891551020482633)
    await channel.send('SnekBot booted up. Hello!')


@client.event
async def on_message(message):
    db.check_user(message, conn)
    global prefix
    global busy

    if message.author == client.user:
        return

    if message.content.startswith(prefix + 'help'):
        await message.channel.send('List of commands :\n```'
        + prefix + 'help : Displays this help page!\n'
        + prefix + 'hello : Says hello!\n'
        + prefix + 'facts : Says some coffee facts!\n'
        + prefix + 'brew : Brews coffee for you!\n'
        + prefix + 'boop : Boop me!\n'
        + prefix + 'boom : Under no circumstancecs you should use this command.'
        + '```')

    if message.content.startswith(prefix + 'hello'):
        async with message.channel.typing():
            await asyncio.sleep(3)
        await message.channel.send('Hello, ' + message.author.mention + '!')

    if message.content.startswith(prefix + 'getid'):
        await message.channel.send('Your ID is : ' + str(message.author.id))

    if message.content.startswith(prefix + 'facts'):
        async with message.channel.typing():
            await asyncio.sleep(5)
        with open('coffeefacts.txt') as f:
            lines = f.readlines()
        await message.channel.send(random.choice(lines))

    if message.content.startswith(prefix + 'brew'):
        randNum = random.randint(0, 14)
        brewMessage = await message.channel.send('Brewing')
        await asyncio.sleep(1)
        await brewMessage.edit(content='Brewing.')
        await asyncio.sleep(1)
        await brewMessage.edit(content='Brewing..')
        await asyncio.sleep(1)
        await brewMessage.edit(content='Brewing...')
        await asyncio.sleep(1)
        if randNum != 7:
            await brewMessage.edit(content=':coffee: Here you go!')
        else:
            await brewMessage.edit(content=':tea: Here you go! ...wait')
            await asyncio.sleep(5)
            await brewMessage.edit(content=':coffee: Here you go! Sorry about that :broken_heart:')

    if message.content.startswith(prefix + 'boop'):
        await message.channel.send('<:googleseviper:745643309669548133>:purple_heart:')

    if message.content.startswith(prefix + 'boom'):
        if(busy == False):
            busy = True
            await message.channel.send(':boom:')
            async with message.channel.typing():
                await asyncio.sleep(3)
            await message.channel.send('Why did you do that, ' + message.author.mention + '?')
            async with message.channel.typing():
                await asyncio.sleep(3)
            await message.channel.send('Going down for repairs. :(')
            await asyncio.sleep(3)
            await client.change_presence(status=discord.Status.offline)
            await asyncio.sleep(12)
            await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=prefix+'help'))
            async with message.channel.typing():
                await asyncio.sleep(3)
            await message.channel.send('Don\'t do that again please :broken_heart:')
            busy = False

    if message.content.startswith(prefix + 'shutdown'):
        if str(message.author.id) == owner_id:
            await message.channel.send('Shutting down. Goodbye!')
            await client.change_presence(status=discord.Status.offline)
            exit()
        else:
            await message.channel.send('Access denied.')

    if message.content.startswith(prefix + 'countdown'):
        if(busy == False):
            busy = True
            countdownMessage = await message.channel.send('3')
            await asyncio.sleep(1)
            await countdownMessage.edit(content='2')
            await asyncio.sleep(1)
            await countdownMessage.edit(content='1')
            await asyncio.sleep(1)
            await countdownMessage.edit(content='GO')
            busy = False
            await asyncio.sleep(15)
            await countdownMessage.edit(content='Countdown finished.')

client.run(token)
