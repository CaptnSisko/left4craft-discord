import redis
import discord
import asyncio

channels = {
        '424870757860900865': 'global',
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
    if not message.author.id == '428260311959601157':
        try:
            if len(message.content) > 256:
                await client.send_message(message.channel, message.author.mention + ' Chat message not sent because the character limit is 256.')
            else:
                r.publish('minecraft.chat.' + channels[message.channel.id] + '.in', '&3[Discord&r' + message.author.top_role.name + '&3]&r ' + message.author.display_name + ' &3&l»&r ' + message.content.replace('&','& ').replace('\n', ' '))
                print('Sending ' + message.author.id + ':' + message.content + ' to ' + channels[message.channel.id])
        except KeyError:
            pass

client.run('')
