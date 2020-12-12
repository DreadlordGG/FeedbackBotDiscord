import os
import discord
from dotenv import load_dotenv
about_text=open("files/about.txt", "r").read()

async def print(message):
    await message.channel.send(about_text)
