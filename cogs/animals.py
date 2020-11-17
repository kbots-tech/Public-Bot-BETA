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
      data = json.load(response)[0]
      image = data['url']
      try:
        data = data['breeds'][0]
      except IndexError:
        data = data['breeds']
      if not data:
        await self.dog(ctx)
      else:
        try:
          fields = [
            ('Weight',f"{data['weight']['imperial']}lbs.",True),
            ('Height',f"{data['height']['imperial']}in.",True),
            ('Breed Group',data['breed_group'] if data['breed_group'] else "N/A",True),
            ('Life Span',data['life_span'],True),
            ('Bred for',data['bred_for'] if data['bred_for']  else 'N/A',False),
            ('Temperament',data['temperament'],False)
          ]
          embed=discord.Embed(title=data['name'])
          embed.set_image(url = image)
          for name,value,inline in fields:
            embed.add_field(name=name,value=value,inline=inline)
          await ctx.send(embed=embed)
        except KeyError:
          await self.dog(ctx)

    @commands.command(pass_contex=True)
    async def cat(self,ctx):
        url = 'https://api.thecatapi.com/v1/images/search'

        response = urllib.request.urlopen(url)
        data = json.load(response)[0]['url']

        embed = discord.Embed(title='Enjoy a cat picture')
        embed.set_image(url=data)
        await ctx.send(embed=embed)
    


# The setup fucntion below is neccesarry. Remember we give bot.add_cog() the name of the class in this case MembersCog.
# When we load the cog, we use the name of the file.
def setup(bot):
    """sets up the cog"""
    bot.add_cog(AnimalCog(bot))
