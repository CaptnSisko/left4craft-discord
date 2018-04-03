import discord
import asyncio
import redis
import json
from hashlib import sha256

r = redis.Redis()
client = discord.Client()

def updateJson(id):
    hash = sha256(id.encode()).hexdigest()[:8]
    print('hash of ' + id + ': ' + hash)
    data = None
    try:
        data = json.loads(r.get('discord.synccodes').decode('utf-8'))
    except KeyError:
        data = {}
    data[hash] = id
    print('discord id for ' + hash + ': ' + data[hash])
    print('data: ' + json.dumps(data))
    r.set('discord.synccodes',json.dumps(data))
    return hash

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(message):
    if message.channel.is_private and not message.author.id == '428260311959601157':
        await client.send_message(message.channel, 'Go ingame and type `/discord ' + updateJson(message.author.id) + '` to sync your account.')

@client.event
async def on_join(member):
    await client.send_message(member, 'Go ingame and type `/discord ' + updateJson(message.author.id) + '` to sync your account.')

client.run('')
