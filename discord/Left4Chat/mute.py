import redis
import discord
import asyncio
import time as t

channelid = ['424870757860900865']

client = discord.Client()
r = redis.Redis()

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    
    muted = []
    p = r.pubsub(ignore_subscribe_messages=True)
    p.subscribe('minecraft.chat.mute')
    server = client.get_server('424571587413540874')
    channels = [client.get_channel(ch) for ch in channelid]
    mute = discord.PermissionOverwrite()
    mute.send_messages = False
    while True:
        try:
            msg = p.get_message()
            if msg:
                data = msg['data'].decode('utf-8')
                uid = data.split(':')[0]
                data = data.split(':')[1].split(' ')
                member = server.get_member(uid)
                print(data)
                if data[1] == 'muted':
                    for ch in channels:
                        await client.edit_channel_permissions(ch, member, mute)
                elif data[1] == 'tempmuted':
                    for ch in channels:
                        time = float(data[4])
                        units = data[5]
                        if units in 'minutes': time *= 60
                        if units in 'hours': time *= 3600
                        if units in 'days': time *= 86400
                        if units in 'months': time *= 2592000
                        if units in 'years': time *= 946080000
                        print('muting ' + member.id + ' for ' + str(time) + ' seconds')
                        await client.edit_channel_permissions(ch, member, mute)
                        muted.append([member,t.time()+time])
                elif data[1] == 'unmuted':
                    print('unmuting ' + member.id)
                    for ch in channels:
                        await client.delete_channel_permissions(ch, member)
            for player in muted:
                if player[1] <= t.time():
                    for ch in channels:
                        print('unmuting ' + player[0].id + ' (timeout)')
                        await client.delete_channel_permissions(ch, player[0])
                    muted.remove(player)
        except:
            print('Error unmuting!!!!!')
        await asyncio.sleep(0.1)

client.run('')

