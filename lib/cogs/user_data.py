from discord.ext import commands
import sqlite3
import lib.bot.emot_util as emot_util
import discord
import lib.bot.message_util as message_util
from discord.utils import get

class EmotionCog(commands.Cog, name='User_Data'):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot or message.author == self.bot.user or message.content.startswith(('$', ';', '!', '/', '&', '@', '%')):
            return

        db = sqlite3.connect('main.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT user_id FROM emotion_data WHERE guild_id = '{message.author.guild.id}'"
                       f"AND user_id = '{message.author.id}'")
        result = cursor.fetchone()
        emotion = emot_util.get_emotion(message.content)

        if result is None:
            sql = ("INSERT INTO emotion_data(guild_id, user_id, joy, sadness, anger, fear, love, surprise) "
                   "VALUES(?, ?, ?, ?, ?, ?, ?, ?)")
            val = (message.author.guild.id, message.author.id, 0, 0, 0, 0, 0, 0)
            cursor.execute(sql, val)
            db.commit()

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
            username = user.display_name
            icon = user.avatar_url
            cursor.close()
            db.close()
        else:
            db = sqlite3.connect('main.sqlite')
            cursor = db.cursor()
            cursor.execute(f"SELECT joy, sadness, anger, fear, love, surprise FROM emotion_data "
                           f"WHERE guild_id = '{ctx.message.guild.id}' AND user_id = '{ctx.message.author.id}'")
            result = cursor.fetchone()
            username = ctx.message.author.display_name
            icon = ctx.message.author.avatar_url
            cursor.close()
            db.close()
        await ctx.send(embed=message_util.embed(user=username, icon=icon, title='__**Emotion Stats**__',
                                                thumbnail='http://discord.com/assets/626aaed496ac12bbdb68a86b46871a1f.svg',
                                                description = f"{emot_util.emoji['joy']} Joy: {str(result[0])}\n"
                                                              f"{emot_util.emoji['sadness']} Sadness: {str(result[1])}\n"
                                                              f"{emot_util.emoji['anger']} Anger: {str(result[2])}\n"
                                                              f"{emot_util.emoji['fear']} Fear: {str(result[3])}\n"
                                                              f"{emot_util.emoji['love']} Love: {str(result[4])}\n"
                                                              f"{emot_util.emoji['surprise']} Surprise: {str(result[5])}"))

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

    @commands.command()
    async def leaderboard(self, ctx, category):
        db = sqlite3.connect('main.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT user_id, {category} FROM emotion_data ORDER BY {category} DESC")
        result = cursor.fetchall()
        leaderboard = ""
        leader = await self.bot.fetch_user(int(result[0][0]))
        for count, row in enumerate(result):
            user = await self.bot.fetch_user(int(row[0]))
            leaderboard += f"{count+1}. **{user.display_name}** - {row[1]}\n"
        await ctx.send(embed=message_util.embed(title=f':trophy:\t{category} Leaderboard\t:trophy:', thumbnail= leader.avatar_url,
        description=leaderboard))



def setup(bot):
    bot.add_cog(EmotionCog(bot))
    print('Emotion Cog is loaded!')