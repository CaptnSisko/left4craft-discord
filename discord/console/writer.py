import redis
import discord
import asyncio
import time
from threading import Thread

ids = [424863503887630337,424863531612110848,424863554366210059,424863574200942593,428230754888056852]
queues = {
        'hub': 0,
        'survival': 1,
        'creative': 2,
        'zombies': 3,
        'build': 4
}
servers = ['hub', 'survival', 'creative', 'zombies', 'build']
client = discord.Client()
queue = [[] for i in range(len(ids))]

def logQueue():
    global queue
    global queues

    r = redis.Redis()
    p = r.pubsub(ignore_subscribe_messages=True)
    for srv in servers:
        p.subscribe('minecraft.console.' + srv + '.out')
        print('Subscribed to ' + srv)
    for msg in p.listen():
        srv = msg['channel'].decode('utf-8').split('.')[2]
        queue[queues[srv]].append(msg['data'].decode('utf-8'))

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
            for srv in queue:
                while srv:
                    try:
                        msg = ''
                        while srv and len(msg) + len(srv[0]) < 2000:
                            msg += srv[0] + '\n'
                            srv.remove(srv[0])
                        print(msg[:-1])
                        await client.send_message(channels[i], msg)
                    except:
                        print('error')
                i += 1
        await asyncio.sleep(0.01)

Thread(target=logQueue).start()
client.run('')
