import discord
from discord import Embed
from DB_Commands import get_data,insert_data
from discord.ext import commands


class DevCommands(commands.Cog, name='admin'):
  '''These are the admin commands'''

  def __init__(self, bot):
	  self.bot = bot

  @commands.command(name='setprefix',
                    brief='Guild admins can use this to set the bot prefix for this server.')
  @commands.has_permissions(administrator=True)
  async def Set_Prefix(self,ctx, prefix):
    if prefix == '.':
      await insert_data("DELETE FROM `prefixes` WHERE guild_id = %s",(ctx.guild.id,))
    else:
      if await get_data('SELECT `prefix` FROM `prefixes` WHERE `guild_id` = %s',(ctx.guild.id,)):
        await insert_data('UPDATE `prefixes` SET `prefix` = %s WHERE `guild_id` = %s',(prefix,ctx.guild.id))
      else:
        await insert_data('INSERT INTO `prefixes`(`guild_id`, `prefix`) VALUES (%s,%s)',(ctx.guild.id,prefix))

    await ctx.send(embed=Embed(title='New Prefix Set',
                               description = f"New prefix is: {prefix}"))


def setup(bot):
	bot.add_cog(DevCommands(bot))