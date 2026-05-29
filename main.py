import discord
from groq import Groq
from dotenv import load_dotenv
import os
import string
import time
import pyttsx3
import http.client
import gen.imagegen as imagegen
import gen.ytdownload as ytdownload
import re
import ticket
import gen.ai
import schedule
import asyncio
import json

async def reset():
    print("dementia!")
    file_path = "log.json"

    if os.path.exists(file_path):
        os.remove(file_path)
        print("memory reset")

async def scheduler_loop():
    while True:
        schedule.run_pending()
        await asyncio.sleep(1)


load_dotenv()
global enable
enable = 0
engine = pyttsx3.init()
Naughty = [
    "add more of these 123abc",
]

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

system_prompt = """

""" #need to make this customizable later









@client.event
async def on_ready():
    global aichannel
    aichannel = client.get_channel(1509952955548307487)

    print(f'We have logged in as {client.user}')

    # schedule the reset
    schedule.every().day.at("12:00").do(
        lambda: asyncio.create_task(reset())
    )

    # start scheduler loop
    client.loop.create_task(scheduler_loop())
@client.event
async def on_message(message):
    global system_prompt


    if message.author == client.user:
        return
    if message.content.startswith('$help'):
        await message.channel.send('''
$help - help
$msgenable - enable/disable the ai
$prompt - change the prompt of the ai
$wipe - wipe the memory (automatically resets at 12:00 CDT)
$spamping - spamping someone
$image - create an image
$talk - tts in vc
$play - play a song (yt) in vc
$stop - stop song in vc
$ticket - create a ticket
----- admin only -----
$adminplace - placeholder
$kick - self-explanatory
$ban - self-explanatory
$resolve - resolves a ticket, use in the ticket channel
        ''')
    elif message.content.startswith('$msgenable'):
        global enable
        if enable == 0:
            enable = 1
            await message.channel.send("ai enabled")
        else:
            enable = 0
            await message.channel.send("ai disabled")

    elif message.content.startswith('$adminplace') and any(role.name == os.environ.get("ADMIN") for role in message.author.roles): # might need to change this
       await message.channel.send('yes mr. sigma')
    elif message.content.startswith('$wipe'):
        if os.path.exists(gen.ai.LOG_FILE):
            os.remove(gen.ai.LOG_FILE)
        await message.channel.send('memory wiped')
        print('memory wiped')
    elif message.content.startswith('$prompt'):
        system_prompt = message.content[len('$prompt '):].strip()
        print("prompt set to: " + system_prompt)
        await message.channel.send('changed to ' + system_prompt)
    elif message.content.startswith('$kick') and any(role.name == os.environ.get("ADMIN") for role in message.author.roles):
        if message.mentions:
            await message.mentions[0].kick()
            await message.channel.send(f'kicked {message.mentions[0]}')
        else:
            await message.channel.send('mention someone idiot')
    elif message.content.startswith('$ban') and any(role.name == os.environ.get("ADMIN") for role in message.author.roles):
        if message.mentions:
            await message.mentions[0].ban()
            await message.channel.send(f'banned {message.mentions[0]}')
        else:
            await message.channel.send('mention someone idiot')
    elif message.content.startswith('$spamping'):
        if message.mentions:
            for i in range(5):
                await message.channel.send(f'{message.mentions[0].mention}')
                time.sleep(1)
        else:
            await message.channel.send('mention someone idiot')
    elif message.content.startswith("$talk"):
        if message.author.voice and message.author.voice.channel:
            voice = message.guild.voice_client
            if voice is None or not voice.is_connected():
                voice = await message.author.voice.channel.connect(timeout=5.0, reconnect=True, cls=discord.voice_client.VoiceClient, self_deaf=False, self_mute=False)
            text = message.content[len('$talk '):].strip()
            engine.save_to_file(text, 'export/output.mp3')
            engine.runAndWait()
            source = discord.FFmpegPCMAudio('export/output.mp3')
            voice.play(source)
        else:
            await message.channel.send("You need to be in a voice channel first!")
    elif message.content.startswith("$play"):
        if message.author.voice and message.author.voice.channel:
            text = message.content[len('$play '):].strip()
            title, uploader = ytdownload.download_audio(text)
            voice = message.guild.voice_client
            if voice is None or not voice.is_connected():
                voice = await message.author.voice.channel.connect(reconnect=True, cls=discord.voice_client.VoiceClient, self_deaf=False, self_mute=False)
            source = discord.FFmpegPCMAudio('export/export.mp3')
            voice.play(source)
            await message.channel.send("Now playing " + title + " by " + uploader)
        else:
            await message.channel.send("You need to be in a voice channel first!")
    elif message.content.startswith("$stop"):
        voice = message.guild.voice_client
        voice.stop()
    elif message.content.startswith('$image'):
        inputimage = message.content[len('$image '):].strip()
        imagegen.imagegen(inputimage)
        await message.channel.send(file=discord.File('output.png'))
    elif message.content.startswith('$ticket'):
        print("ticket was made")
        await message.delete()
        await ticket.makechannel(message)
    elif message.content.startswith('$resolve') and any(role.name == os.environ.get("ADMIN") for role in message.author.roles):
        print("resovled")
        if message.channel.name.startswith('ticket'):
            await message.channel.delete()
        else:
            await message.channel.send("be in a ticket")
    elif message.content.startswith('$'):
        await message.channel.send('unknown command use $help')
    


    #censorship
    else:
        content = message.content.lower()
        words = [w.strip(string.punctuation) for w in content.split()]
        naughty_set = {w.lower() for w in Naughty}
        if any(word in naughty_set for word in words):
            await message.delete()
            await message.channel.send('no')


    if enable == 1 and message.channel == aichannel:
        await gen.ai.callAI(system_prompt, message)




client.run(os.environ.get("DISCORD_BOT_TOKEN"))
