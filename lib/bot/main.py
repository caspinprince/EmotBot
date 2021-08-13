import os
from dotenv import load_dotenv
from discord.ext import commands
import emot_util
import sqlite3
import sys
import traceback

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='$')

@bot.event
async def on_ready():
    db = sqlite3.connect('main.sqlite')
    cursor = db.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS main(
        guild_id TEXT,
        msg TEXT,
        channel_id TEXT
        );
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS emotion_data(
            "guild_id"	TEXT,
            "user_id"	INTEGER,
            "joy"	INTEGER,
            "sadness"	INTEGER,
            "anger"	INTEGER,
            "fear"	INTEGER,
            "love"	INTEGER,
            "surprise"	INTEGER
        );
    ''')
    print(f'{bot.user} has connected to Discord!')

initial_extensions = ['lib.cogs.user_data']
if __name__ == '__main__':
    for extension in initial_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            print(f'Failed to load extension {extension}', file=sys.stderr)
            traceback.print_exc()


@bot.command(name = 'emotion')
async def emotion(ctx):
    if ctx.author == bot.user:
        return
    emotion = emot_util.get_emotion(ctx.message.content)
    await ctx.send(emot_util.emoji[emotion])

bot.run(TOKEN)



