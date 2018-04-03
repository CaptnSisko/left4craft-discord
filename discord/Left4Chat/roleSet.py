import discord
import asyncio
import redis
from threading import Thread

r = redis.Redis()
client = discord.Client()

ranks = {
        '429026758692438038': 'Guest',
        '424866580141441026': 'User',
        '424866580141441026': 'User+',
        '424866580141441026': 'Donor',
        '426469168171319297': 'Patron',
        '424867110041288716': 'Patron+',
        '424867526481281024': 'Builder',
        '424867726511570955': 'Helper',
        '424867915226021888': 'Moderator',
        '424868133967364096': 'Admin',
        '424868296886583316': 'Owner',
        '424867647381831690': 'Staff'
}

async def handle_msg(msg,server,roles):
    msg = msg['data'].decode('utf-8')
    cmd = msg.split(' ')
    uid = cmd[1]
    member = discord.Server.get_member(server,uid)
    if cmd[0] == 'setuser':
        nick = cmd[2]
        print('Giving user ' + uid + ' nickname ' + nick)
        await client.change_nickname(member,nick)
    elif cmd[0] == 'setgroup':
        group = cmd[2]
        print('Setting rank for ' + uid + ' to ' + roles[group].id)
        await client.replace_roles(member, roles[group])
        if group in ['Helper','Moderator','Admin','Owner']:
            await client.replace_roles(member, roles[group],roles['Staff'])
        else:
            await client.replace_roles(member, roles[group])
        for role in member.roles: print(role.name)
    else:
        print('Error parsing command ' + cmd + '!')

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    p = r.pubsub(ignore_subscribe_messages=True)
    p.subscribe('discord.botcommands')
    server = client.get_server('424571587413540874')
    roles = {}
    for role in server.roles:
        try:
            roles[ranks[role.id]] = role
        except KeyError:
            pass
    while True:
        msg = p.get_message()
        if msg:
            try:
                await handle_msg(msg,server,roles)
            except:
                print('Error!')
        await asyncio.sleep(0.1)

client.run('')
