"""Commands for the trivia module"""
import discord
from discord.ext import commands
import json
import urllib.request
import random
import asyncio
from DB_Commands import get_data, insert_data

tokenID = ""

class TriviaCog(commands.Cog,name='trivia'):
    """
    Commands for the Trivia Questions
    """

    def __init__(self, bot):
        self.bot = bot


    @commands.command(
        name="trivia",
        brief="grabs a question from a random category and allows you to answer",
    )
    async def trivia(self, ctx):
        quiz_var = random.randrange(9, 32)

        data = [6]
        data = url_request(quiz_var)
        embed = discord.Embed(title="TRIVIA",)

        embed.add_field(name="Category:", value=data[0], inline=True)
        embed.add_field(name="Difficulty", value=data[1], inline=True)
        embed.add_field(name="Question", value=data[2], inline=False)
        embed.add_field(name="1: " + data[3], value="______", inline=False)
        embed.add_field(name="2: " + data[4], value="______ ", inline=False)
        embed.add_field(name="3: " + data[5], value="______ ", inline=False)
        embed.add_field(name="4: " + data[6], value="______ ", inline=False)
        embed.set_footer(text="Choose your answers, you have 15 seconds")
        message = await ctx.send(embed=embed)
        await message.add_reaction("1️⃣")
        await message.add_reaction("2️⃣")
        await message.add_reaction("3️⃣")
        await message.add_reaction("4️⃣")
        await asyncio.sleep(15)
        message = await self.bot.get_channel(ctx.channel.id).fetch_message(message.id)

        if data[7]==1:
          entrants = [u for u in await message.reactions[0].users().flatten() if not u.bot]
        elif data[7]==2:
          entrants = [u for u in await message.reactions[1].users().flatten() if not u.bot]
        elif data[7]==3:
          entrants = [u for u in await message.reactions[2].users().flatten() if not u.bot]
        elif data[7]==4:
          entrants = [u for u in await message.reactions[3].users().flatten() if not u.bot]

        if len(entrants) > 0:  
            names = ""
            for f in entrants:
              names = names+(f"{f.name}, ")
              if await get_data("SELECT * FROM `scores` WHERE id = %s",(f.id,)):
                await insert_data("UPDATE `scores` SET `score`=`score`+10 WHERE %s",(f.id,))
              else:
                await insert_data("INSERT INTO `scores`(`id`, `score`) VALUES (%s,%s)",(f.id,10))
            message = await ctx.send(embed=discord.Embed(title=f"Congrats {names} got it right",description="use !score to check your score and !trivia stats to check the leaderboard!",))
        else:
            message = await ctx.send(embed=discord.Embed(title="No one got the right answer",description=f"The correct answer was {data[7]}, react with ✅ to play again",))
        await message.add_reaction("✅")
        def check(reaction, user):
            return reaction.message.channel == ctx.channel and not user.bot
        try:
          reaction, user = await self.bot.wait_for('reaction_add', timeout= 15, check=check)
          if reaction.emoji:
            await self.trivia(ctx)
        except asyncio.TimeoutError:
            await ctx.send(embed=discord.Embed(title="No one wanted to play again",))
  

    #This command prints your scores
    @commands.command(
        name="score",
        brief="returns your score",
    )
    async def score(self,ctx):
      score = (await get_data("SELECT `score` FROM `scores` WHERE  `id` = %s",(ctx.author.id,)))
      if not score:
        score = 0
      embed = discord.Embed(title=f"Your Score, {ctx.author.name}",description=f"{score[0][0]} points",)
      await ctx.send(ctx.author.mention,embed=embed)

    @commands.command(
        name="leaderboard",
        brief="returns bot trivia leaderboard",
    )
    async def leaderboard(self,ctx):
      data = await get_data("SELECT `id`, `score` FROM `scores` ORDER BY `score` DESC")
      leaders=""
      for count,info in enumerate(data[:10],1):
        print(info[0])
        leaders += f"**{count}** {self.bot.get_user(int(info[0])).name} with {info[1]} points\n"
      embed = discord.Embed(title="Leaderboard",description=leaders,)
      await ctx.send(embed=embed)
      



def url_request(value: int):
    """takes in a value for the category of the question and returns an array with the info for the question"""
    global tokenID
    url = (
        "https://opentdb.com/api.php?amount=1&category="
        + str(value)
        + "&type=multiple&token="
        + tokenID
    )

    response = urllib.request.urlopen(url)
    data = json.load(response)
    responsecode = data["response_code"]
    if str(responsecode) == "4":
        url2 = "https://opentdb.com/api_token.php?command=reset&token=" + tokenID

    elif str(responsecode) == "3":
        url2 = "https://opentdb.com/api_token.php?command=request"
        response2 = urllib.request.urlopen(url2)
        data2 = json.load(response2)
        tokenID = data2["token"]
        data = url_request(value)
        return data
    else:
        question = data["results"]
        for f in question:
            data[0] = f["category"]
            data[1] = f["difficulty"]
            correct_answer = f["correct_answer"]
            answers = f["incorrect_answers"]
            data[2] = f["question"]

        answers.append(correct_answer)

        random.shuffle(answers)

        correct = correct_answer

        answers[0] = answers[0].replace("&#039;", "'")
        answers[1] = answers[1].replace("&#039;", "'")
        answers[2] = answers[2].replace("&#039;", "'")
        answers[3] = answers[3].replace("&#039;", "'")

        if answers[0] == correct:
            correct = 1
        if answers[1] == correct:
            correct = 2
        if answers[2] == correct:
            correct = 3
        if answers[3] == correct:
            correct = 4

        answers[0] = answers[0].replace("&amp;", "&")
        answers[1] = answers[1].replace("&amp;", "&")
        answers[2] = answers[2].replace("&amp;", "&")
        answers[3] = answers[3].replace("&amp;", "&")

        data[3] = answers[0]
        data[4] = answers[1]
        data[5] = answers[2]
        data[6] = answers[3]
        data[7] = correct

        data[2] = data[2].replace("&quot;", '"')
        data[2] = data[2].replace("&#039;", "'")

        return data

def setup(bot):
    """Load the bot Cog"""
    bot.add_cog(TriviaCog(bot))