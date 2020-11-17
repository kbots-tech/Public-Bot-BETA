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
              if cog_name != 'Developer Commands':
                if  len(cog.get_commands()):
                    embed.add_field(
                        name=cog_name, inline=True,
                        value=' - '.join(sorted(f'`{c.name}`' for c in cog.get_commands()))
                    )
        else:
          embed = discord.Embed(title=f"Commands for {args}")
          for command in (self.bot.get_cog(args)).get_commands():
            embed.add_field(name=command.name,value=command.brief,inline=True) 


        await ctx.send(embed=embed)
  
  @commands.command(
      name='ping',
        brief='returns bot latency'
        )
  async def ping(self,ctx):
    await ctx.send(f'Pong! {round(self.bot.latency *1000)}ms')


def setup(bot):
	bot.add_cog(help(bot))