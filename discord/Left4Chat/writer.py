import redis
import discord
import asyncio
from threading import Thread

ids = [424870757860900865]
queues = {
        'global': 0
}
channels = ['global']

client = discord.Client()
queue = [[] for i in range(len(ids))]

def logQueue():
    global queue
    global queues

    r = redis.Redis()
    p = r.pubsub(ignore_subscribe_messages=True)
    for ch in channels:
        p.subscribe('minecraft.chat.' + ch + '.out')
        print('subscribed to ' + ch)
    for msg in p.listen():
        ch = msg['channel'].decode('utf-8').split('.')[2]
        queue[queues[ch]].append(msg['data'].decode('utf-8'))

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

    global queue
    global ids
    channels = [client.get_channel(str(ids[i])) for i in range(len(ids))]
    while True:
        i = 0
        while i < len(queue):
            for ch in queue:
                while ch:
                    try:
                        msg = ''
                        while ch and len(msg) + len(ch[0]) < 2000:
                            msg += ch[0] + '\n'
                            ch.remove(ch[0])
                        print(ch[:-1])
                        await client.send_message(channels[i], msg)
                    except:
                        print('error')
                i += 1
        await asyncio.sleep(0.01)

Thread(target=logQueue).start()
client.run('')
