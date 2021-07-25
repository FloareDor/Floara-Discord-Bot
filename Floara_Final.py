import discord
from discord.ext import commands, tasks
import pickle
import random as rand

from chat_cog import chat_cog
from reddit_cog import reddit_cog
from translate_cog import translate_cog
from mod_cog import mod_cog
from music_cog import music_cog

real_date_cleared = []
status = ['Nurture', 'Titanfall 2', 'Planetside 2', 'a DJ set']
messagecounts = {}

client = commands.Bot(command_prefix = ">")

client.add_cog(mod_cog(client))
client.add_cog(translate_cog(client))
client.add_cog(chat_cog(client))
client.add_cog(reddit_cog(client))
client.add_cog(music_cog(client))

@client.event
async def on_ready():
    print("Bot is ready af")
    change_status.start()

# Chaning the status
@tasks.loop(seconds = 60)
async def change_status():
    await client.change_presence(activity = discord.Game(rand.choice(status)))

# Logging the messages
@client.event
async def on_message(message):
        #if message.guild.id not in messagecounts.keys(): # Make sure there's already an entry... If not, add one!
            #messagecounts[message.guild.id] = 0
        #messagecounts[message.guild.id] += 1
    with open('messagecountsdata.p', 'rb') as fp:
        messagecounts = pickle.load(fp)
    uniquecode = f"{message.guild.id}#{message.author.id}"
    if '865441153893269545' != uniquecode.split("#")[1]:
        if uniquecode not in messagecounts.keys():
            messagecounts[uniquecode] = 0
        messagecounts[uniquecode] += 1
        #print(messagecounts)
    print(messagecounts)
    id = f"<@!{message.author.id}>"
    print(message.clean_content)
    with open('messagecountsdata.p', 'wb') as fp:
        pickle.dump(messagecounts, fp, protocol=pickle.HIGHEST_PROTOCOL)
        print(messagecounts)
    await client.process_commands(message)

# Running the bot
TOKEN = ""
with open("token.txt") as file:
    TOKEN = file.read()
client.run(TOKEN)