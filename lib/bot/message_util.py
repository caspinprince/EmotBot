import discord

def embed(user=None, icon=None, title=None, description=None, footer=None, thumbnail=None):
    embed=discord.Embed(
        title = title,
        description= description,
        color=discord.Color.blue())
    if user is not None and icon is not None:
        embed.set_author(name=user, icon_url=icon)
    if thumbnail is not None:
        embed.set_thumbnail(url=thumbnail)
    if footer is not None:
        embed.set_footer(text=footer)
    return embed