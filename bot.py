# bot.py
import os
import discord
from dotenv import load_dotenv
import FeedbackBotDB
import sqlalchemy as db
import modules.admin, modules.requests, modules.help, modules.users, modules.about

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

    #help section
    if message.content.startswith('$help'):
        await modules.help.print_user(message)
    if  message.content.startswith('$help') and message.author.guild_permissions.administrator and message.channel.name == 'feedback-control':
        await modules.help.print_admin(message)

    #about section
    if message.content.startswith('$about'):
        await modules.about.print(message)
    if message.content.startswith('$feedback'):
        await modules.requests.feedback(client,message,FeedbackBotDB)

    ### Initial configuration for server ###
    if  message.content.startswith('$init') and message.author.guild_permissions.administrator and message.channel.name == 'feedback-control':
        await modules.admin.init(client,message)
client.run(TOKEN)
