import discord
from discord.ext import commands
from discord.flags import alias_flag_value

from youtube_dl import YoutubeDL


class music_cog(commands.Cog):

    def __init__(self,client):
        self.client = client

        self.is_playing = False

        # we store the channel as the second parameter in the music_queue (2D list)
        self.music_queue = []
        self.YDL_OPTIONS = {'format':'bestaudio', 'noplaylist':'True'}
        self.FFMPEG_OPTIONS =  {'before_options':'-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options':'-vn'}
        
        self.vc = ""
    
    def search_yt(self, name):
        with YoutubeDL(self.YDL_OPTIONS) as ydl:
            try:
                info = ydl.extract_info("ytsearch:%s" % name, download = False)['entries'][0]
            except Exception:
                return False
        return {'source': info['formats'][0]['url'], 'title': info['title']}
    
    def play_next(self):
        if len(self.music_queue) > 0:
            self.is_playing = True

            m_url = self.music_queue[0][0]['source']

            self.music_queue.pop(0)

            self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after = lambda e: self.play_next())
        else:
            self.is_playing = False

    async def play_music(self):
        if len(self.music_queue) > 0:
            self.is_playing = True

            m_url = self.music_queue[0][0]['source']
            
            if self.vc == "" or not self.vc.is_connected():
                # connecting to the music queue
                self.vc = await self.music_queue[0][1].connect() 
            else:
                self.vc = await self.client.move_to(self.music_queue[0][1])

            # print(self.music_queue)

            self.music_queue.pop(0)

            self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after = lambda e: self.play_next())
        else:
            self.is_playing = False
    
    @commands.command(alias = "play")
    async def p(self,ctx,*args):
        query = " ".join(args)

        voice_channel = ctx.message.author.voice.channel
        if voice_channel is None:
            await ctx.send("Please connect to a voice channel")
        else:
            song = self.search_yt(query)
            
            if type(song) == type(True):
                await ctx.send("Could not load the song..it could be a playlist or a livestream")
            else:
                await ctx.send("Song added to the queue")
                self.music_queue.append([song,voice_channel])

                if self.is_playing != True:
                    await self.play_music()
    
    @commands.command()
    async def q(self,ctx):
        retval = ""
        for i in range(0, len(self.music_queue)):
            retval += self.music_queue[i][0]['title'] + "\n"
        print(retval)
        if retval != "":
            await ctx.send(retval)
        else:
            await ctx.send("No songs in da queue")
    
    @commands.command()
    async def pause(self,ctx):
        if self.vc != "":
            self.vc.pause()
            await ctx.send("Song paused!")
    
    @commands.command()
    async def resume(self,ctx):
        if self.vc != "":
            self.vc.resume()
            await ctx.send("Resumed!")

    @commands.command()
    async def skip(self, ctx):
        if self.vc != "":
            self.vc.stop()
            await self.play_music()
    
    @commands.command()
    async def leave(self, ctx):
        if self.vc != "":
            self.vc.stop()
        self.music_queue.clear()
        guild = ctx.message.guild
        voice_client = guild.voice_client
        await voice_client.disconnect()

        
