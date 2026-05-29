import asyncio
from datetime import datetime, timedelta
from groq import Groq
from dotenv import load_dotenv
import discord
import re
from . import imagegen
import os
import json

LOG_FILE = "log.json"
clientgroq = Groq(api_key=os.environ.get("GROQ_API_KEY"))
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
async def callAI(system_prompt, message):
    if not message.content.startswith('$'):
        global completion
        completion = clientgroq.chat.completions.create(
            messages=[
                {
                "role": "system",
                "content": system_prompt + "also, if you feel that you aren't involved in the message (like if a person is talking to another person), use [NORESPONSE] to not respond. Only say[NORESPONSE], otherwise it will not pick it up. Do this semi-rarely, like when it is explicitly said that they are talking to another. You could also chime in if you feel it's right.",
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
            await message.channel.send(file=discord.File('export/output.png'))
        if ai_response == "[NORESPONSE]":
                pass
        else:
            await message.channel.typing()
            await message.channel.send(clean_response)
            

