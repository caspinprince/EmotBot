import os
import requests
import discord
import json
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

emotions = {'joy': ':smile:',
            'sadness': ':cry:',
            'anger': ':angry:',
            'fear': ':cold_sweat:',
            'love': ':smiling_face_with_3_hearts:',
            'surprise': ':astonished:'}

client = discord.Client()

def get_emotion(string):
    response = requests.post('https://EmotionAPI.matthewzhang8.repl.co/predict', json =[string])
    emotion = response.json()
    return(emotion['prediction'][0])

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    emotion = get_emotion(message.content)
    await message.channel.send(emotions[emotion])

client.run(TOKEN)

