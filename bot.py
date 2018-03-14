import discord
import asyncio # I don't actually think I need this...
import re
import random

#import hashlib
#import string
#import random
#import json


# User data object
class Citizen:
    name = ""
    identity = ""
    money = 0
    dockyards = 0
    
    def __init__(self, n, i, m):
        self.name = n
        self.identity = i
        self.money = m
        # self.dockyards = d

# User data arrays
# citizens for simplified searching, citizen_objects to store actual objects
citizens = []
citizen_objects = []

# Read in user data from users file
def create_users():
    with open('users', 'r') as f:
        print('USERS:')
        for line in f:
            print(line.rstrip().split('/'))
            obj = line.rstrip().split('/')
            citizen_objects.append(Citizen(obj[0], obj[1], int(obj[2]), int(obj[3])))
            citizens.append(obj[0])
        print()
        
# update users file with user data
def update_users():
   with open('users', 'r+') as f:
       index = 0
       for line in f:
           current = citizen_objects[index]
           line.replace(line, current.name + '/' + current.identity + '/' + str(current.money) + "\n")
           print(current.name + '/' + current.identity + '/' + str(current.money) + "\n")
           index += 1
       print()
    
def test():
    for item in citizen_objects:
        print(item.name + " " + str(item.money))

# TODO
def thought_crime(msg):
    return msg

# By T. Knuth
def random_line(afile):
    line = next(afile)
    for num, aline in enumerate(afile):
      if random.randrange(num + 2): continue
      line = aline
    return line

# Setup
client = discord.Client()

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content.startswith("!evaporate") and message.author.roles:
        if "Administrator" == message.author.top_role.name:
            # print(message.content[11:])
            server = message.server
            die = "EVAPORATING USER " + message.content[11:]
            await client.send_message(message.channel, die)
            await client.kick(server.get_member_named(message.content[11:]))
            return
        else:
            nah = "INSUFFICIENT AUTHORITY"
            await client.send_message(message.channel, nah)
            return
                
    if message.author.display_name not in citizens:
        citizen_objects.append(Citizen(message.author.display_name, message.author.id, 100))
        citizens.append(message.author.display_name)
        msg = "USER (" + message.author.display_name + "), A PROFILE HAS BEEN CREATED FOR YOU, DESIGNATED " + message.author.id
        with open('users', 'a') as f:
            f.write(message.author.display_name + '/' + message.author.id + '/' + '100' + "\n")
        await client.send_message(message.channel, msg)
   
    #thought_crime(message.content)
    
    democracy_pattern = r'd\s*e\s*m\s*o\s*c\s*r\s*a\s*c\s*y'
    js_pattern = r'j\s*a\s*v\s*a\s*s\s*c\s*r\s*i\s*p\s*t'
    js_pattern_simple = r'j\s`*s'
    sleep_pattern = r'sleep'

    
    if re.search(democracy_pattern, message.content, re.IGNORECASE) is not None:
        warning = "THOUGHT CRIME DETECTED\nUSER "  + message.author.display_name + ", NUMBER " + message.author.id + "\nBY USING THE WORD DEMOCRACY YOU ARE GUILTY OF CRIMETHINK"
        await client.send_message(message.channel, warning)
    elif re.search(js_pattern, message.content, re.IGNORECASE) is not None or re.search(js_pattern_simple, message.content, re.IGNORECASE) is not None:
        warning = "THOUGHT CRIME DETECTED\nUSER "  + message.author.display_name + ", NUMBER " + message.author.id + "\nJAVASCRIPT IS FOR FUCKING IDIOTS"
        await client.send_message(message.channel, warning)
    elif re.search(sleep_pattern, message.content, re.IGNORECASE) is not None:
        mhe = "Sleep is Righteousness\nBut the world wakes\nWe are made in the image of the world"
        await client.send_message(message.channel, mhe)
    
    
    if message.content.startswith('!me'):
        msg = 'YOU ARE USER ' +  message.author.id + ' | DESIGNATED ' + message.author.display_name.format(message)
        await client.send_message(message.channel, msg)
    elif message.content.startswith('!nuke'):
         msg = 'TARGETING ' + message.content[6:].format(message)
         await client.send_message(message.channel, msg)
    elif message.content.startswith('!help'):
        msg = 'Remember, you are not alone | National Suicide Prevention Lifeline: 1-800-273-8255'.format(message)
        await client.send_message(message.channel, msg)
    elif message.content.startswith('!onii-sama'):
        with open('weeb.txt', 'r') as f:
            line = random_line(f)
        msg = line.format(message)
        await client.send_message(message.channel, msg)
    elif message.content.startswith('!credit'):
        for user in citizen_objects:
            print(message.author.display_name + " " + user.name)
            if message.author.display_name == user.name:
                money = 'USER ' + message.author.display_name + ", YOU HAVE " + str(user.money) + " :dollar:".format(message)
                await client.send_message(message.channel, money)
                break
    elif message.content.startswith('!give'):
        if "Administrator" == message.author.top_role.name:
            for user in citizen_objects:
                command = message.content.rsplit(' ', 1)
                if command[0][6:] == user.name:
                    user.money += int(command[1])
                    update_users()
        else:
            await client.send_message(message.channel, 'Why would you be able to give yourself money?')
            
    elif message.content.startswith('!secret admin thing'):
        test()
        
    elif message.content.startswith('!inventory'):
        await client.send_file(message.channel, "carrier.png", content="F")
        await client.send_file(message.channel, "battleship.png", content="U")
        await client.send_file(message.channel, "heavy_cruiser.png", content="C")
        await client.send_file(message.channel, "destroyer.png", content="K")
        await client.send_file(message.channel, "submarine.png", content="S")
            
@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    
# =============================================================================
#     for server in client.servers: 
#         for channel in server.channels: 
#                 # Channels on the server
#                 if channel.permissions_for(server.me).send_messages:
#                     await client.send_message(channel, "I AM ONLINE\nAND\nI\nSEE\nYOU")
#                     # So that we don't send to every channel:
#                     break
# =============================================================================
    
if __name__ == "__main__":
    create_users()
    client.run("NDIwMTE1MzY5NTU5MzI2NzIx.DX5-dA.PI3m899g76WveeKgNMdZcMPssCU")