import discord
from discord import Embed
from discord.ext import commands


class help(commands.Cog, name='stats'):

  def __init__(self, bot):
      self.bot = bot
      self.bot.remove_command('help')

  @commands.command()
  async def getuser(self,ctx,args=""):
    if args:
      user = self.bot.get_user(int(args[3:-1]))
    else: user = ctx.author
    embed = Embed(title = f"Stats for {user.name}",descrtiption=f"Summoned by {ctx.author.name}",color=user.color) 
    embed.set_thumbnail(url = user.avatar_url)
    fields={
      ('Name',user.name,True),
      ('ID',user.id,True),
      
          }
    for name,value,inline in fields:
      embed.add_field(name=name,value=value,inline=inline)
    await ctx.send(embed=embed)


def setup(bot):
	bot.add_cog(help(bot))