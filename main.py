import os
from discord import Embed
from keep_alive import keep_alive
from discord.ext import commands
from DB_Commands import get_data,insert_data

async def get_prefix(bot,message):
  prefix = await get_data('SELECT `prefix` FROM `prefixes` WHERE `guild_id` = %s',(message.guild.id,))
  return prefix[0] if prefix else "."


bot = commands.Bot(
	command_prefix='*',  # Change to desired prefix
	case_insensitive=True  # Commands aren't case-sensitive
)


@bot.event
async def on_guild_leave(guild):
  if await get_data('SELECT `prefix` FROM `prefixes` WHERE `guild_id` = %s',(guild.id,)):
    await insert_data('DELETE FROM `prefixes` WHERE `guild_id` = %s',(guild.id,))


bot.author_id = 480055359462178826  # Change to your discord id!!!

@bot.event 
async def on_ready():  # When the bot is ready
    print("I'm in")
    print(bot.user)  # Prints the bot's username and identifier


extensions = [
	'cogs.cog_example','cogs.admin', 'cogs.weather','cogs.last_fm','cogs.stats','cogs.animals','cogs.help'  # Same name as it would be if you were importing it
]

if __name__ == '__main__':  # Ensures this is the file being ran
	for extension in extensions:
		bot.load_extension(extension)  # Loades every extension.

keep_alive()  # Starts a webserver to be pinged.
bot.run(os.environ.get('token'))  # Starts the bot