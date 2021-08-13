from discord.ext import commands
import sqlite3
import lib.bot.emot_util as api_call
import discord

class EmotionCog(commands.Cog, name='User_Data'):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user or message.content.startswith(('$', ';', '!', '/', '&', '@', '%')):
            return

        db = sqlite3.connect('main.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT user_id FROM emotion_data WHERE guild_id = '{message.author.guild.id}'"
                       f"AND user_id = '{message.author.id}'")
        result = cursor.fetchone()
        emotion = api_call.get_emotion(message.content)

        if result is None:
            sql = ("INSERT INTO emotion_data(guild_id, user_id, joy, sadness, anger, fear, love, surprise) "
                   "VALUES(?, ?, ?, ?, ?, ?, ?, ?)")
            val = (message.author.guild.id, message.author.id, 0, 0, 0, 0, 0, 0)
            cursor.execute(sql, val)
            db.commit()
        else:
            cursor.execute(f"SELECT user_id, {emotion} FROM emotion_data "
                           f"WHERE guild_id = '{message.author.guild.id}'"
                           f"AND user_id = '{message.author.id}'")
            result1 = cursor.fetchone()
            current_value = int(result1[1])
            sql = (f"UPDATE emotion_data SET {emotion} = ? WHERE guild_id = ? AND user_id = ?")
            val = (current_value+1, str(message.guild.id), str(message.author.id))
            cursor.execute(sql, val)
            db.commit()

    @commands.command()
    async def stats(self, ctx, user:discord.User = None):
        if user is not None:
            db = sqlite3.connect('main.sqlite')
            cursor = db.cursor()
            cursor.execute(f"SELECT joy, sadness, anger, fear, love, surprise FROM emotion_data "
                           f"WHERE guild_id = '{ctx.message.guild.id}' AND user_id = '{user.id}'")
            result = cursor.fetchone()
            await ctx.send(str(result[0]))
            cursor.close()
            db.close()
        elif user is None:
            db = sqlite3.connect('main.sqlite')
            cursor = db.cursor()
            cursor.execute(f"SELECT joy, sadness, anger, fear, love, surprise FROM emotion_data "
                           f"WHERE guild_id = '{ctx.message.guild.id}' AND user_id = '{ctx.message.author.id}'")
            result = cursor.fetchone()
            await ctx.send(f">>> __**Emotion Stats for {ctx.message.author.display_name}**__\n\n"
                           f"Joy: {str(result[0])}\nSadness: {str(result[1])}\nAnger: {str(result[2])}\n"
                           f"Fear: {str(result[3])}\nLove: {str(result[4])}\nSurprise: {str(result[5])}")
            cursor.close()
            db.close()

    @commands.command()
    async def reset(self, ctx):
        db = sqlite3.connect('main.sqlite')
        cursor = db.cursor()
        sql = (f"UPDATE emotion_data SET joy = ?, sadness = ?, anger = ?, fear = ?, love = ?, surprise = ?"
               f"WHERE guild_id = ? AND user_id = ?")
        val = (0, 0, 0, 0, 0, 0, str(ctx.message.guild.id), str(ctx.message.author.id))
        try:
            cursor.execute(sql, val)
            db.commit()
            await ctx.send(':white_check_mark: User stats were reset!')
        except Exception as e:
            await ctx.send(':x: User stats could not be reset!')
        cursor.close()
        db.close()

def setup(bot):
    bot.add_cog(EmotionCog(bot))
    print('Emotion Cog is loaded!')