import os

import discord

# import json
# import requests
# from keep_alive import keep_alive
# COMMAND_PREFIX = "&"
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)


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
            await message.channel.send("Uh Uh max spam limit is capped at 100")
        else:
            for _ in range(n):
                await message.channel.send(f"{msg.split()[2:]}")
            await message.channel.send(f"Succesfully spammed {n} times")


if __name__ == "__main__":
    token = os.environ.get("TOKEN")
    if not token:
        raise RuntimeError("TOKEN is required")
    client.run(token)
