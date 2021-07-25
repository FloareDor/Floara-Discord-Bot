from asyncio.windows_events import NULL
from typing import Optional
import discord
from discord import client
from discord.embeds import Embed
from discord.errors import NotFound
from discord.ext import commands
from discord.member import Member
import requests as req
from datetime import datetime
import pickle
date_cleared = "dd"
real_date_cleared = []

now = datetime.now()
class mod_cog(commands.Cog):
    @commands.command()

    async def ban(self,ctx, member: discord.Member, *, reason =None):
        if member == None or member == ctx.message.author:
            await ctx.channel.send("You cannot ban yourself")
            return
        if reason == None:
            reason = "for being a bad guy"
        message = f"You have been banned from {ctx.guild.name} for {reason}"
        #await ctx.guild.ban(member, reason=reason)
        try:
            await member.send(message)
            await member.ban(reason = reason)
            await ctx.channel.send(f"{member} is banned!")
        except discord.ext.commands.errors.MemberNotFound:
            await ctx.channel.send(f"{member} is not in the server")

    @commands.command()
    async def kick(self,ctx, member: discord.Member, *, reason = None):
        if reason == None:
            reason = "for being a bad guy"
        message = f"You have been kicked from {ctx.guild.name} for {reason}"
        await member.send(message)
        await member.kick(reason = reason)
        await ctx.send(f'User {member} has been kicked')

    @commands.command()
    async def create_invite(self,ctx):
        """Create instant invite"""
        link = await ctx.channel.create_invite(max_age = 300)
        await ctx.send(link)

    @commands.command(pass_context = True)
    async def send_invite(self,ctx, user: discord.User, *, message = None):
        link = await ctx.channel.create_invite(max_age = 300)
        await user.send(link)

    @commands.command()
    async def unban(self,ctx, *, member):
        #print("yes")
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')
        print(member_name, member_discriminator)
        for ban_entry in banned_users:
            user = ban_entry.user
            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.channel.send(f"Unbanned: {user.mention}")
                link = await ctx.channel.create_invite(max_age = 300)
                await member.send(f"You have been unbanned from {ctx.guild.name}")
                user = await client.get_user_info(member)
                print(user)
                await user.send(link)

    @commands.command()
    async def getname(self,ctx, member: discord.Member):

        await ctx.send(f'User name: {member.name}, id: {member.id}')

        with req.get(member.avatar_url_as(format='png')) as r:
            img_data = r.content
        with open(f'{member.name}.png', 'wb') as f:
            f.write(img_data)
    @commands.command()
    async def useinfo(ctx, *, user: discord.Member = None): # b'\xfc'
        if user is None:
            user = ctx.author      
        date_format = "%a, %d %b %Y %I:%M %p"
        embed = discord.Embed(color=0xdfa3ff, description=user.mention)
        embed.set_author(name=str(user), icon_url=user.avatar_url)
        embed.set_thumbnail(url=user.avatar_url)
        embed.add_field(name="Joined", value=user.joined_at.strftime(date_format))
        members = sorted(ctx.guild.members, key=lambda m: m.joined_at)
        embed.add_field(name="Join position", value=str(members.index(user)+1))
        embed.add_field(name="Registered", value=user.created_at.strftime(date_format))
        if len(user.roles) > 1:
            role_string = ' '.join([r.mention for r in user.roles][1:])
            embed.add_field(name="Roles [{}]".format(len(user.roles)-1), value=role_string, inline=False)
        perm_string = ', '.join([str(p[0]).replace("_", " ").title() for p in user.guild_permissions if p[1]])
        embed.add_field(name="Guild permissions", value=perm_string, inline=False)
        embed.set_footer(text='ID: ' + str(user.id))
        return await ctx.send(embed=embed)

    @commands.command(name = "userinfo" , alias_flag_value = "ui")
    async def userinfo(self,ctx, target: Optional[Member]):
        target = target or ctx.author
        embed = Embed(title="User Information",
                    colour = target.colour,
                    timestamp = datetime.utcnow())
        fields = [("Name", str(target), True),
                    ("ID", target.id, True), 
                    ("Bot?", target.bot, True),
                    ("Top Role", target.top_role.mention, True),
                    ("Status", str(target.status).title(), True),
                    # ("Activity", f"{str(target.activity.type).split('.')[-1].title()} {target.activity.name}", True),
                    ("Created on", target.created_at.strftime("%d/%m/%Y %H/%M/%S"), True),
                    ("Joined at", target.joined_at.strftime("%d/%m/%Y %H/%M/%S"), True),
                    ("Boosted", bool(target.premium_since), True)]
        for name, value, inline in fields:
            embed.add_field(name = name, value = value, inline = inline)
            
        embed.set_thumbnail(url = target.avatar_url)
        await ctx.send(embed = embed)


    @commands.command(description="Mutes the specified user.")
    #@commands.has_permissions(manage_messages=True)
    async def mute(self,ctx, member: discord.Member, *, reason=None):
        guild = ctx.guild
        mutedRole = discord.utils.get(guild.roles, name="Muted")

        if not mutedRole:
            mutedRole = await guild.create_role(name="Muted")

            for channel in guild.channels:
                await channel.set_permissions(mutedRole, speak=False, send_messages=False, read_message_history=True, read_messages=False)
        embed = discord.Embed(title="muted", description=f"{member.mention} was muted ", colour=discord.Colour.light_gray())
        embed.add_field(name="reason:", value=reason, inline=False)
        await ctx.send(embed=embed)
        await member.add_roles(mutedRole, reason=reason)
        await member.send(f" you have been muted from: {guild.name} reason: {reason}")

    @commands.command(description="Unmutes a specified user.")
    #@commands.has_permissions(manage_messages=True)
    async def unmute(self,ctx, member: discord.Member):
        mutedRole = discord.utils.get(ctx.guild.roles, name="Muted")

        await member.remove_roles(mutedRole)
        await member.send(f" you have unmutedd from: - {ctx.guild.name}")
        embed = discord.Embed(title="unmute", description=f" unmuted-{member.mention}",colour=discord.Colour.light_gray())
        await ctx.send(embed=embed)

    

    @commands.command()
    async def clearshit(self,ctx):
        date_cleared = str(datetime.now())
        real_date_cleared.append(date_cleared)
        print(date_cleared)
        #date_cleared = str(datetime.now())
        with open('messagecountsdata.p', 'rb') as fp:
            messagecounts = pickle.load(fp)
            messagecounts.clear()
            with open('messagecountsdata.p', 'wb') as fp:
                pickle.dump(messagecounts, fp, protocol=pickle.HIGHEST_PROTOCOL)
        


        # dd/mm/YY H:M:S
        #dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        #print("date and time =", dt_string)
        await ctx.send("Cleared shit")

    @commands.command()
    async def serverstats(self,ctx):
        with open('messagecountsdata.p', 'rb') as fp:
            messagecounts = pickle.load(fp)
        embed=discord.Embed(title=f"{ctx.guild.name}")
        embed.add_field(name="Users:", value=ctx.guild.member_count, inline=False)
        embed.add_field(name="Channels:", value=len(ctx.guild.channels), inline=False)
        try:
            x = [int(messagecounts[id]) for id in messagecounts if str(ctx.guild.id) in id]
            embed.add_field(name="Messages sent:", value = sum(x), inline=False)
            if len(real_date_cleared) != 0:
                embed.add_field(name="Since:", value = real_date_cleared[len(real_date_cleared)-1].split('.')[0], inline = False)
            else:
                embed.add_field(name="Since:", value = str(now).split('.')[0], inline = False)
        except KeyError:
            pass    
        #print(messagecounts)
        await ctx.send(embed=embed)
    @commands.command()
    async def activestats(self,ctx):
        with open('messagecountsdata.p', 'rb') as fp:
            messagecounts = pickle.load(fp)
        embed = discord.Embed(title = f"{ctx.guild.name}")
        try:
            try:
                sno = 1
                for userid in messagecounts:
                    if str(ctx.guild.id) == userid.split("#")[0]:
                        user = f"<@!{userid}>"
                        username = await ctx.guild.fetch_member(userid.split('#')[1])
                        print(username)
                        print(username)
                        if username != 'Floara#2335':
                            embed.add_field(name = f"{sno}) {username}", value = f"{messagecounts[userid]} messages", inline = False)
                            sno+=1
                            print(messagecounts)
                #await ctx.send(f'%s : {messagecounts[userid]} ' % user)
            except NotFound:
                pass
        except KeyError:
            pass
        await ctx.send(embed = embed)