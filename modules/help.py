import os
import discord
from dotenv import load_dotenv
help_text=open("files/help.txt", "r").read()
help_text_admin=open("files/admin.txt", "r").read()

async def print_user(message):
    await message.channel.send(help_text)
    
async def print_admin(message):
    await message.channel.send(help_text_admin)
