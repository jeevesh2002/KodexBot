import discord
import os
from discord import client
from discord import channel
from discord import message
import json
import requests
from keep_alive import keep_alive
COMMAND_PREFIX = "&"
client = discord.Client()

@client.event
async def on_ready():
    print("Bot is awake")
@client.event
async def on_message(message):
    msg = message.content
    if message.author.bot:
        return
    if msg.startswith("spam"):
        n = int(msg.split()[1])
        if n > 100:
            await message.channel.send(f"Uh Uh max spam limit is capped at 100")
        else:
            for i in range(n):
                await message.channel.send(f"{msg.split()[2:]}")
            await message.channel.send(f"Succesfully spammed {n} times")
client.run("ODU0MjExMzg3MTM1NzU0MzEw.YMgoWQ.tmTcFpwgygGsYv6AhLpW9GOH2Eo")
