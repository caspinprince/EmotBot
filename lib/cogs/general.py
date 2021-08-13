from discord.ext import commands
import discord
import lib.bot.message_util as message_util
import lib.bot.emot_util as emot_util

class GeneralCog(commands.Cog, name='general'):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def info(self, ctx):
        await ctx.send(embed=message_util.embed(user=self.bot.user.display_name,icon=self.bot.user.avatar_url,
                                                title='Info', footer ='More info at: github.com/caspinprince/EmotBot',
                                                description='EmotBot is a friendly discord bot that detects the emotion of any message '
                                                            'sent in this server! Run the `$help` command to see a list of available commands.'))

    @commands.command()
    async def help(self, ctx):
        await ctx.send(embed=message_util.embed(user=self.bot.user.display_name,icon=self.bot.user.avatar_url, title='Commands Help',
                                                description='**$help**: List commands and usage details.\n'
                                                            '**$info**: Display general information about the bot.\n'
                                                            '**$emotion** <message>: Reacts to the message with an emoji of the predicted emotion.\n'
                                                            '**$stats** <@user>: Gets the saved emotion data for the specified user. If no user is '
                                                            'specified, personal data is shown.\n'
                                                            '**$reset**: Resets personal saved emotion data to starting values.\n'
                                                            '**$leaderboard** <emotion>: Shows the leaderboard for a specific emotion.',
                                                footer='To suggest changes or new features DM @matthew_z #6969.'))

    @commands.command()
    async def emotion(self, ctx, *, text=None):
        if ctx.author == self.bot.user:
            return
        if text is None:
            await ctx.send(':x: Please enter a message!')
        else:
            emotion = emot_util.get_emotion(text)
            await ctx.send(emot_util.emoji[emotion])

def setup(bot):
    bot.add_cog(GeneralCog(bot))
    print('General Cog is loaded!')



