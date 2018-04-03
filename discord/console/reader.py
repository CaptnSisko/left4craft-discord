import redis
import discord
import asyncio

servers = {
        '424863503887630337': 'hub',
        '424863531612110848': 'survival',
        '424863554366210059': 'creative',
        '424863574200942593': 'zombies',
        '428230754888056852': 'build'
}


client = discord.Client()
r = redis.Redis()

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(message):
    if not message.author.top_role.name == 'ROBOAT':
        try:
            r.publish('minecraft.console.' + servers[message.channel.id] + '.in', message.content)
            if message.content.lower() == 'stop' or message.content.lower() == 'restart':
                r.set('minecraft.console.' + servers[message.channel.id] + '.panic', '')
            print('Sending ' + message.content + ' to ' + servers[message.channel.id])
        except KeyError:
            pass

client.run('')
