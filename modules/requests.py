import os
import discord
from dotenv import load_dotenv
import FeedbackBotDB
import sqlalchemy as db

async def post(client,message,FeedbackBotDB):
        pass
async def edit(client,message,FeedbackBotDB):
        pass
async def getFeedback(client,message,FeedbackBotDB):
        pass
async def need(client,message,FeedbackBotDB):
        pass
async def recent(client,message,FeedbackBotDB):
        pass
async def feedback(client,message,FeedbackBotDB):
        if len(message.content) - 14 <= FeedbackBotDB.get_data(message.guild.id)[0].min_length:
            await message.channel.send("Too short")
        else:
            await message.channel.send("Good")
