#!/usr/bin/env python3
import os
import discord
from dotenv import load_dotenv
import FeedbackBotDB
import sqlalchemy as db
load_dotenv()
async def init(client,message):
        def check(m):
             return m.channel == channel and m.author.name == author
        def check_y_n(m):
             return m.channel == channel and m.author.name == author and ( m.content == 'Y' or m.content == 'n' )
        author = message.author.name
        channel = message.channel
        config={}
        config['guild'] = message.guild.id

        # Get category name
        await message.channel.send("Category name?")
        msg = await client.wait_for('message', check=check)
        config['category'] = msg.content
        
        # Get channel name
        await message.channel.send("Channel name?")
        msg = await client.wait_for('message', check=check)
        config['channel'] = msg.content

        # Get minimum message lenght
        await message.channel.send("Min lenght?")
        msg = await client.wait_for('message', check=check)
        config['min_lenght'] = msg.content

        # Get minimum message lenght
        await message.channel.send("Maximum of feedback before closure?")
        msg = await client.wait_for('message', check=check)
        config['max_feedback'] = msg.content

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
                overwrites = {
                     message.guild.default_role: discord.PermissionOverwrite(read_messages=True,send_messages=False),
                     message.guild.me: discord.PermissionOverwrite(read_messages=True,send_messages=True)
                }
                await message.guild.create_text_channel(config['rules_channel_name'],category=category,overwrites=overwrites)
        if general_channel is None:
            await message.guild.create_text_channel(config['channel'],category=category)
        FeedbackBotDB.push_data(config['guild'],config['category'],config['channel'],config['min_lenght'],config['max_feedback'])

