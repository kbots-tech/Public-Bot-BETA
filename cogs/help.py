import discord
from discord.ext import commands


class help(commands.Cog, name='help'):

  def __init__(self, bot):
      self.bot = bot
      self.bot.remove_command('help')

  @commands.command(name='help', brief="List every command of the bot")
  async def all_commands(self, ctx,*,args=""):
        """ Provide a list of every command available command for the user,
        split by extensions and organized in alphabetical order.
        Will not show the event-only extensions """
        if not args:
          embed = discord.Embed(
              title='All commands', description='\n'.join(
                  (f'Use `{ctx.prefix}help *cog*` to find out more about a cog !',
                  f'> `{len(self.bot.commands)}` commands available')
              )
          )
        

          for cog_name, cog in self.bot.cogs.items():
              if  len(cog.get_commands()):
                  embed.add_field(
                      name=cog_name, inline=False,
                      value=' - '.join(sorted(f'`{c.name}`' for c in cog.get_commands()))
                  )
        else:
          embed = discord.Embed(title=f"Commands for {args}")
          for command in (self.bot.get_cog(args)).get_commands():
            embed.add_field(name=command.name,value=command.brief,inline=False) 


        await ctx.send(embed=embed)


def setup(bot):
	bot.add_cog(help(bot))