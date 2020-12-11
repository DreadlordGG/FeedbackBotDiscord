# bot.py
import os
import discord
from dotenv import load_dotenv
import FeedbackBotDB
import sqlalchemy as db
help_text=open("help.txt", "r").read()
help_text_admin=open("admin.txt", "r").read()
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
guild = os.getenv('DISCORD_SERVER')
client = discord.Client()
engine = db.create_engine('sqlite:///FeedbackBot.db')
connection = engine.connect()
metadata = db.MetaData()
census = db.Table('server', metadata, autoload=True, autoload_with=engine)
@client.event

async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_guild_join(guild):
    print('We have joined the {0} server'.format(guild))
    print(guild)
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
        
        author = message.author.name
        channel = message.channel
        config={}
        config['guild'] = message.guild.id
        
        # Get category name
        await message.channel.send("Category name?")
        def check(m):
            return m.channel == channel and m.author.name == author
        def check_y_n(m):
            return m.channel == channel and m.author.name == author and ( m.content == 'Y' or m.content == 'n' )
        
        msg = await client.wait_for('message', check=check)
        config['category'] = msg.content

        # Get channel anme
        await message.channel.send("Channel name?")
        msg = await client.wait_for('message', check=check)
        config['channel'] = msg.content

        # Get minimum message lenght
        await message.channel.send("Min lenght?")
        msg = await client.wait_for('message', check=check)
        config['min_lenght'] = msg.content

        # Create rules channe
        await message.channel.send("Create rules channel?[Y/n]")
        msg = await client.wait_for('message', check=check_y_n)
        config['rules_channel'] = msg.content

        #Rules channel name and content
        if config['rules_channel'] == 'Y':
            await message.channel.send("Rules channel name?")
            msg = await client.wait_for('message', check=check)
            config['rules_channel_name'] = msg.content
            await message.channel.send("Set theh rules")
            msg = await client.wait_for('message', check=check)
            config['rules_text'] = msg.content
        else:
            config['rules_channel_name'] = ''
            config['rules_text'] = ''

        #Do the work now
        general_channel = discord.utils.get(message.guild.channels, name=config['channel'])
        general_category = discord.utils.get(message.guild.channels, name=config['category'])
        if general_category is None:
            category = await message.guild.create_category_channel(config['category'])
        if config['rules_channel_name']:
            feedback_channel = discord.utils.get(message.guild.channels, name=config['rules_channel_name'])
            if feedback_channel is None:
                await message.guild.create_text_channel(config['rules_channel_name'],category=category)
        if general_channel is None:
            await message.guild.create_text_channel(config['channel'],category=category)
        FeedbackBotDB.push_data(config['guild'],config['category'],config['channel'],config['min_lenght'])

client.run(TOKEN)
