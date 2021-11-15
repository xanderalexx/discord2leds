import discord
import RPi.GPIO as g
import time
import os
from datetime import datetime, timedelta
from tabulate import tabulate
from threading import Thread

starttime = datetime.now()

g.setmode(g.BCM)

led1 = 25
led2 = 16
led3 = 21
led4 = 12
led5 = 20


def get_temp():
    cpu_temp = os.popen("vcgencmd measure_temp").readline()
    temp1 = cpu_temp.replace("temp=", "")
    return temp1.replace("'C", "")

g.setwarnings(False)

g.setup(led1, g.OUT)
g.setup(led2, g.OUT)
g.setup(led3, g.OUT)
g.setup(led4, g.OUT)
g.setup(led5, g.OUT)
g.output(led1, g.LOW)
g.output(led2, g.LOW)
g.output(led3, g.LOW)
g.output(led4, g.LOW)
g.output(led5, g.LOW)

g.output(led1, g.HIGH)
time.sleep(0.1)
g.output(led2, g.HIGH)
time.sleep(0.1)
g.output(led3, g.HIGH)
time.sleep(0.1)
g.output(led4, g.HIGH)
time.sleep(0.1)
g.output(led5, g.HIGH)
time.sleep(0.1)
g.output(led1, g.LOW)
time.sleep(0.1)
g.output(led2, g.LOW)
time.sleep(0.1)
g.output(led3, g.LOW)
time.sleep(0.1)
g.output(led4, g.LOW)
time.sleep(0.1)
g.output(led5, g.LOW)

masterdata = []
monitoring = False
toptemp = 0

def gettimedif(b):
    return (b-starttime).total_seconds()

def startMonitoring():
    while True:
        global toptemp
        time1 = datetime.now()
        cputemp = float(get_temp())
        if(toptemp == 0):
            toptemp = cputemp
        else:
            if(cputemp > toptemp):
                toptemp = cputemp
            else:
                return
        time.sleep(15)

def updateLeds(num):
    x = 0
    while(x < 5):
        g.output(led1, g.HIGH)
        g.output(led2, g.HIGH)
        g.output(led3, g.HIGH)
        g.output(led4, g.HIGH)
        g.output(led5, g.HIGH)
        time.sleep(0.1)
        g.output(led1, g.LOW)
        g.output(led2, g.LOW)
        g.output(led3, g.LOW)
        g.output(led4, g.LOW)
        g.output(led5, g.LOW)
        time.sleep(0.1)
        x = x + 1
    if(num >= 1):
        g.output(led1, g.HIGH)
    if(num >= 2):
        g.output(led2, g.HIGH)
    if(num >= 3):
        g.output(led3, g.HIGH)
    if(num >= 4):
        g.output(led4, g.HIGH)
    if(num >= 5):
        g.output(led5, g.HIGH)

client = discord.Client()
voice = discord.VoiceClient(client, 846969663794446360)

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    global monitoring
    if(monitoring == False):
        monitoring = True
        t1 = Thread(target = startMonitoring)
        t1.setDaemon(True)
        t1.start()

@client.event
async def on_message(message):
    global toptemp
    if message.author == client.user:
        return
    if(len(message.mentions) == 0):
        return
    if(message.mentions[0] == client.user):
        if("!" in message.content):
            if("uptime" in message.content):
                secondsalive = gettimedif(datetime.now())
                await message.channel.send(timedelta(seconds=secondsalive))
            elif("temp" in message.content and "toptemp" not in message.content):
                final = get_temp() + "C"
                await message.channel.send(get_temp() + "C")
            elif("toptemp" in message.content):
                final = str(toptemp) + "C"
                await message.channel.send(str(toptemp) + "C")
            else:
                return
        else:
            return
    else:
        return
            
        
@client.event
async def on_voice_state_update(member, before, after):
        if(before.channel == after.channel):
            return
        if(member.voice == None):
            #await client.get_channel(846969663794446359).send(member.name + " has left")
            print(member.name + " has left")
        else:
            #await client.get_channel(846969663794446359).send(member.name + " has joined")
            print(member.name + " has joined")
        try:
            updateLeds(len(after.channel.members))
        except:
            updateLeds(len(before.channel.members))

client.run('NjQzMzUyOTM0ODU1NDc1MjAw.XckPHA.JEZgQhBeQFX9E0p4g2vsB3zix70')

