from asyncio.windows_events import NULL
import discord
from discord.ext import commands
import praw
import random as rand

search_limit = 50
reddit = praw.Reddit(
    client_id= 'mQiQTwEKfmKtDSWq0jHzyg',
    client_secret= 'DrZG-CKbOkkGAzhSp59B5X3zAYu0tQ',
    user_agent='<console:FLOARE:1.0>',
    check_for_async=False
)
class reddit_cog(commands.Cog):
    def steal(self,subReddit):
        all_subs = []
        #await ctx.send("Here's your meme, take it and leave.")
        subreddit = reddit.subreddit(subReddit)
        for submission in subreddit.hot(limit=search_limit):
            all_subs.append(submission)
            #print(submission.title)
        random_sub = rand.choice(all_subs)
        name = random_sub.title
        url = random_sub.url
        l = len(url)
        if url[-3:l] == "jpg" or url[-3:l] == "png" or url[-3:l] == "jpeg":
            emb = discord.Embed(title = name)
            emb.set_image(url = url)
            text = None
            if rand.randrange(0,4) == 3:
                text = rand.choice(["Here's your meme. Have a great day! : )", "Here's your meme. Take it and leave : )", "Your order has been delivered : )", "Fresh memes boiz", "Here's a fresh hot hot meme for you..", "Finding da best memes...."])
            return emb,text
        else:
            return self.steal(subReddit)
        #await ctx.send(embed = emb)
    @commands.command()
    async def meme(self,ctx):
        emb,text = self.steal("memes")
        if text!=None:
            await ctx.send(text)
        await ctx.send(embed = emb)
    @commands.command()
    async def earthme(self,ctx):
        ball_subs = []
        #await ctx.send("Here's your meme, take it and leave.")
        subreddit = reddit.subreddit("EarthPorn")
        for submission in subreddit.hot(limit=search_limit):
            ball_subs.append(submission)
            #print(submission.title)
        random_sub = rand.choice(ball_subs)
        name = random_sub.title
        url = random_sub.url
        emb = discord.Embed(title = name[0:-16] + " : )")
        emb.set_image(url = url)
        await ctx.send(embed = emb)
    @commands.command()
    async def amongusmeme(self,ctx):
        emb,text = self.steal("AmongUsMemes")
        if text!=None:
            await ctx.send(text)
        await ctx.send(embed = emb)
    @commands.command()
    async def valomeme(self,ctx):
        emb,text = self.steal("ValorantMemes")
        if text!=None:
            await ctx.send(text)
        await ctx.send(embed = emb)
    @commands.command()
    async def f1meme(self,ctx):
        emb,text = self.steal("F1Memes")
        if text!=None:
            await ctx.send(text)
        await ctx.send(embed = emb)
    #@commands.command()
    #async def music(self,ctx):
        #ball_subs = []
        #await ctx.send("Here's your meme, take it and leave.")
        #subreddit = reddit.subreddit("Music")
        #for submission in subreddit.hot(limit=20):
            #ball_subs.append(submission)
            #print(submission.title)
        #random_sub = rand.choice(ball_subs)
        #name = random_sub.title
        #url = random_sub.url
        #emb = discord.Embed(title = name)
        #emb.set_image(url = url)
        #await ctx.send(embed = emb)
    @commands.command()
    async def synthhelp(self,ctx,*, arg):
        subreddit = reddit.subreddit("synthrecipes")
        for submission in subreddit.hot(limit = search_limit):
            if str(arg).lower() in submission.title.lower():
                if submission.comments != NULL:
                    await ctx.send(embed = discord.Embed(title = submission.title))
                    for comment in submission.comments:
                        if hasattr(comment, "body"):
                            comment_lower = comment.body.lower()
                            #print("-----------")
                            await ctx.send(comment.body)
    @commands.command()
    async def quoteme(self,ctx):
        ball_subs = []
        #await ctx.send("Here's your meme, take it and leave.")
        subreddit = reddit.subreddit("quotes")
        for submission in subreddit.hot(limit=search_limit):
            ball_subs.append(submission)
            #print(submission.title)
        random_sub = rand.choice(ball_subs)
        name = random_sub.title
        url = random_sub.url
        emb = discord.Embed(title = name)
        #emb.set_image(url = url)
        await ctx.send(embed = emb)
    # translator
