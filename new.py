import discord
from groq import Groq
from dotenv import load_dotenv
import os
import string
import time
import pyttsx3
import http.client
import imagegen
import ytdownload
import re

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

import json

LOG_FILE = "log.json"

def logging(userinput, ai_response):
    data = []

    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            data = json.load(f)

    data.append({"role": "user", "content": userinput})
    data.append({"role": "assistant", "content": ai_response})

    with open(LOG_FILE, "w") as f:
        json.dump(data, f, indent=2)


def logread():
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            return json.load(f)
    return []


clientgroq = Groq(api_key=os.environ.get("GROQ_API_KEY"))
@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

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
$wipe - wipe the memory
$spamping - spamping someone
$image - create an image
$talk - tts in vc
$play - play a song (yt) in vc
$stop - stop song in vc
----- admin only -----
$adminplace - placeholder
$kick - self-explanatory
$ban - self-explanatory
        ''')
    elif message.content.startswith('$msgenable'):
        global enable
        if enable == 0:
            enable = 1
            await message.channel.send("ai enabled")
        else:
            enable = 0
            await message.channel.send("ai disabled")

    elif message.content.startswith('$adminplace') and (message.author.name == 'j33zx' or message.author.name == 'saulgoodman3516'): # might need to change this
       await message.channel.send('yes mr. sigma')
    elif message.content.startswith('$wipe'):
        if os.path.exists(LOG_FILE):
            os.remove(LOG_FILE)
        await message.channel.send('memory wiped')
        print('memory wiped')
    elif message.content.startswith('$prompt'):
        system_prompt = message.content[len('$prompt '):].strip()
        print("prompt set to: " + system_prompt)
        await message.channel.send('changed to ' + system_prompt)
    elif message.content.startswith('$kick') and (message.author.name == 'j33zx' or message.author.name == 'saulgoodman3516'):
        if message.mentions:
            await message.mentions[0].kick()
            await message.channel.send(f'kicked {message.mentions[0]}')
        else:
            await message.channel.send('mention someone idiot')
    elif message.content.startswith('$ban') and (message.author.name == 'j33zx' or message.author.name == 'saulgoodman3516'):
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

    if enable == 1:
        if not message.content.startswith('$'):
            global completion
            completion = clientgroq.chat.completions.create(
                messages=[
                    {
                    "role": "system",
                    "content": system_prompt + "also, if you feel that you aren't involved in the message (like if a person is talking to another person), use [NORESPONSE] to not respond. Only use [NORESPONSE], otherwise it will not pick it up. Do this semi-rarely, like when it is explicitly said that they are talking to another. You could also chime in if you feel it's right. if you want to make an image out of something, type your prompt out in curly brackets at the end of your message. usually include it with some sort of message. be specific on all fronts, from the position of the camera to how just everything looks in general. when creating an image, don't use something like 'a closeup shot of me blah blah,' you have to describe yourself (EX:'A black haired man is blah blah'). you don't have to do this every time.",
                    },
                    *logread(),
                    {
                    "role": "user",
                    "content": message.author.name + ": " + message.content
                    }
                ], 
            model="llama-3.3-70b-versatile",

            )
            global userinput
            ai_response = completion.choices[0].message.content
            print(message.author.name + ": " + message.content)
            print("AI response:",completion.choices[0].message.content)
            userinput = message.author.name + ": " + message.content
            logging(userinput, ai_response)

            curly_match = re.search(r'\{(.+?)\}', ai_response)
            curly_content = curly_match.group(1) if curly_match else None

            clean_response = re.sub(r'\{.+?\}', '', ai_response).strip()

            if curly_content:
                inputimage = curly_content
                imagegen.imagegen(inputimage)
                await message.channel.send(file=discord.File('/export/output.png'))
            if ai_response == "[NORESPONSE]":
                 pass
            else:
                await message.channel.typing()
                await message.channel.send(clean_response)
            




client.run(os.environ.get("DISCORD_BOT_TOKEN"))