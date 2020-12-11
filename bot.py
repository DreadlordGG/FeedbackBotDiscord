# bot.py
import os
import discord
from dotenv import load_dotenv
import FeedbackBotDB
import sqlalchemy as db
import modules.admin
help_text=open("help.txt", "r").read()
help_text_admin=open("admin.txt", "r").read()
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
guild = os.getenv('DISCORD_SERVER')
client = discord.Client()
#engine = db.create_engine('sqlite:///backends/FeedbackBot.db')
#connection = engine.connect()
#metadata = db.MetaData()
#census = db.Table('server', metadata, autoload=True, autoload_with=engine)

@client.event
async def on_guild_join(guild):
    overwrites = {
    guild.default_role: discord.PermissionOverwrite(read_messages=False),
    guild.me: discord.PermissionOverwrite(read_messages=True,send_messages=True)
}
    admin_channel = discord.utils.get(guild.text_channels, name='feedback-control')
    general_channel = discord.utils.get(guild.text_channels, name='feedback')
    if admin_channel is None:
       await guild.create_text_channel('feedback-control', overwrites=overwrites)

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith('$feedback') and message.channel.name == 'feedback':
        if len(message.content) - 14 <= FeedbackBotDB.get_data(message.guild.id)[0].min_length:
            print(len(message.content))
            await message.channel.send("Too short")
        else:
            await message.channel.send("Good")
    if message.content.startswith('$help') and message.channel.name == 'feedback':
        await message.channel.send(help_text)
    if  message.content.startswith('$help') and message.author.guild_permissions.administrator and message.channel.name == 'feedback-control':
        await message.channel.send(help_text_admin)
    
    ### Initial configuration for server ###
    if  message.content.startswith('$init') and message.author.guild_permissions.administrator and message.channel.name == 'feedback-control':
        await modules.admin.init(client,message)
client.run(TOKEN)
