"""Commands for the animal module"""
import discord
from discord.ext import commands
from settings import weather_token
import json
import urllib.request
from settings import embed_color


class AnimalCog(commands.Cog,name='animals'):
    """commands for the animal finder"""
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_contex=True)
    async def dog(self,ctx):
      url = 'https://api.thedogapi.com/v1/images/search'

      response = urllib.request.urlopen(url)
      data = json.load(response)[0]['breeds']
      if not data:
        await self.dog(ctx)
      else:
        await ctx.send(data)

    @commands.command(pass_contex=True)
    async def cat(self,ctx):
        url = 'https://api.thecatapi.com/v1/images/search'

        response = urllib.request.urlopen(url)
        data = json.load(response)
        print(data)
        for f in data:
          image= f['url']
        await ctx.send(image)
    


# The setup fucntion below is neccesarry. Remember we give bot.add_cog() the name of the class in this case MembersCog.
# When we load the cog, we use the name of the file.
def setup(bot):
    """sets up the cog"""
    bot.add_cog(AnimalCog(bot))
