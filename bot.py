import os
import discord
import pytz

import contextlib
from datetime import datetime, timedelta
from discord.ext import commands


bot = commands.Bot(command_prefix='-')
bot.remove_command('help')

@bot.event
async def on_voice_state_update(member, before, after):
    if before.channel == after.channel:
        return
    
    with contextlib.suppress(Exception):
        for category in before.channel.guild.categories:
            if category.name == '⭐ Custom Channels':
                for channel in category.voice_channels:
                    if not channel.members and not channel_exception(channel.name):
                        if channel.created_at < datetime.utcnow():          
                          await channel.delete(reason="Empty Temp Channel")
    
    if after.channel is not None:
        if after.channel.name.startswith('🔑'):
            await auto_room(member, after.channel)

async def auto_room(member, channel):
    '''Auto room creation function'''
    cat = discord.utils.get(member.guild.categories, name='⭐ Custom Channels')  
    channelName = member.display_name + "'s Channel"
    newChannel = await member.guild.create_voice_channel(channelName, overwrites={
                    member.guild.default_role: discord.PermissionOverwrite(connect=True, speak=True),
                    member: discord.PermissionOverwrite(manage_channels=True, mute_members=True, deafen_members=True, connect=True, speak=True)
                    },
                    category=cat)
    await member.move_to(newChannel, reason='Temp Channel')

# Prevents deletion of Autoroom creation channel
def channel_exception(channel_name):
    if channel_name == '🔑 Materials Generator':
          return True

@bot.command()
async def lock(ctx):
    '''Locks voice channel'''
    if ctx.message.channel.name != 'command-logs':
        log = discord.utils.get(ctx.message.guild.channels, name='solo-leaderboard')
        eembed = errorembed(description='**{0} Command can only be used in {1}**'.format(userMention, log.mention))
        return await ctx.send(embed=eembed)
    else:
        overwrite = discord.PermissionOverwrite(connect=False)
        try:
            channel = ctx.message.author.voice.channel
            if ctx.message.author.permissions_in(channel).manage_channels:
                await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
                embed = discord.Embed(description='{0} You have successfully locked the voice channel.'.format(ctx.message.author.mention))
                embed.color = discord.Color.green()
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(description='{0} You are not the owner of the voice channel.'.format(ctx.message.author.mention))
                embed.color = discord.Color.red()   
                await ctx.send(embed=embed)     
        except:
            embed = discord.Embed(description='{0} You are not connected to any voice channel.'.format(ctx.message.author.mention))
            embed.color = discord.Color.red()
            await ctx.send(embed=embed)

@bot.command()
async def unlock(ctx):
    '''Unlocks voice channel'''
    if ctx.message.channel.name != 'command-logs':
        log = discord.utils.get(ctx.message.guild.channels, name='solo-leaderboard')
        eembed = errorembed(description='**{0} Command can only be used in {1}**'.format(userMention, log.mention))
        return await ctx.send(embed=eembed)
    else:    
        overwrite = discord.PermissionOverwrite(connect=True)
        try:
            channel = ctx.message.author.voice.channel
            if ctx.message.author.permissions_in(channel).manage_channels:
                await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
                embed = discord.Embed(description='{0} You have successfully unlocked the voice channel.'.format(ctx.message.author.mention))
                embed.color = discord.Color.green()
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(description='{0} You are not the owner of the voice channel.'.format(ctx.message.author.mention))
                embed.color = discord.Color.red()   
                await ctx.send(embed=embed)    
        except:
            embed = discord.Embed(description='{0} You are not connected to any voice channel.'.format(ctx.message.author.mention))
            embed.color = discord.Color.red()
            await ctx.send(embed=embed)

@bot.command()
async def deny(ctx, member:discord.Member):
    '''Deny User access to voice channel'''
    if ctx.message.channel.name != 'command-logs':
        log = discord.utils.get(ctx.message.guild.channels, name='solo-leaderboard')
        eembed = errorembed(description='**{0} Command can only be used in {1}**'.format(userMention, log.mention))
        return await ctx.send(embed=eembed)
    else:    
        overwrite = discord.PermissionOverwrite(connect=False)
        channel = ctx.message.author.voice.channel
        if ctx.message.author.permissions_in(channel).manage_channels:   
            await channel.set_permissions(member, overwrite=overwrite)
            embed = discord.Embed(description='{0} You have successfully denied {1} to access the voice channel.'.format(ctx.message.author.mention, member.mention))
            embed.color = discord.Color.green()
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(description='{0} You are not the owner of the voice channel.'.format(ctx.message.author.mention))
            embed.color = discord.Color.red()   
            await ctx.send(embed=embed)
          
@deny.error
async def deny_error(ctx, error):
    if isinstance(error, commands.CommandInvokeError):
        # Bad Argument
        if 'target parameter' in str(error):
            embed = discord.Embed(description='{0} Please tag the user you wish to deny access.'.format(ctx.message.author.mention))
            embed.color = discord.Color.red()   
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(description='{0} You are not connected to any voice channel.'.format(ctx.message.author.mention))
            embed.color = discord.Color.red()   
            await ctx.send(embed=embed)        
    elif isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(description='{0} Please indicate which user you wish to deny access.'.format(ctx.message.author.mention))
        embed.color = discord.Color.red()   
        await ctx.send(embed=embed)

@bot.command()
async def allow(ctx, member:discord.Member):
    '''Grant User access to voice channel'''
    if ctx.message.channel.name != 'command-logs':
        log = discord.utils.get(ctx.message.guild.channels, name='solo-leaderboard')
        eembed = errorembed(description='**{0} Command can only be used in {1}**'.format(userMention, log.mention))
        return await ctx.send(embed=eembed)
    else:    
        overwrite = discord.PermissionOverwrite(connect=True)
        channel = ctx.message.author.voice.channel
        if ctx.message.author.permissions_in(channel).manage_channels:   
            await channel.set_permissions(member, overwrite=overwrite)
            embed = discord.Embed(description='{0} You have successfully granted {1} to access the voice channel.'.format(ctx.message.author.mention, member.mention))
            embed.color = discord.Color.green()
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(description='{0} You are not the owner of the voice channel.'.format(ctx.message.author.mention))
            embed.color = discord.Color.red()   
            await ctx.send(embed=embed)

@allow.error
async def allow_error(ctx, error):
    if isinstance(error, commands.CommandInvokeError):
        # Bad Argument
        if 'target parameter' in str(error):
            embed = discord.Embed(description='{0} Please tag the user you wish to allow access.'.format(ctx.message.author.mention))
            embed.color = discord.Color.red()   
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(description='{0} You are not connected to any voice channel.'.format(ctx.message.author.mention))
            embed.color = discord.Color.red()   
            await ctx.send(embed=embed)        
    elif isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(description='{0} Please indicate which user you wish to allow access.'.format(ctx.message.author.mention))
        embed.color = discord.Color.red()   
        await ctx.send(embed=embed)

@bot.command()
async def kick(ctx, member:discord.Member):
    '''Kicks a User and move to Dumpster Bin'''
    if ctx.message.channel.name != 'command-logs':
        log = discord.utils.get(ctx.message.guild.channels, name='solo-leaderboard')
        eembed = errorembed(description='**{0} Command can only be used in {1}**'.format(userMention, log.mention))
        return await ctx.send(embed=eembed)
    else:    
        dump = discord.utils.get(ctx.message.guild.channels, name='💤 AFK')
        channel = ctx.message.author.voice.channel
        if ctx.message.author.permissions_in(channel).manage_channels:
            if member in channel.members:
                await member.move_to(dump, reason = 'Kicked out of Channel')
                embed = discord.Embed(description='{0} You have successfully kicked {1} out of the voice channel.'.format(ctx.message.author.mention, member.mention))
                embed.color = discord.Color.green()
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(description='{0} {1} is not present in the voice channel.'.format(member.mention, ctx.message.author.mention))
                embed.color = discord.Color.red()   
                await ctx.send(embed=embed)   
        else:
            embed = discord.Embed(description='{0} You are not the owner of the voice channel.'.format(ctx.message.author.mention))
            embed.color = discord.Color.red()   
            await ctx.send(embed=embed)

@kick.error
async def kick_error(ctx, error):
    if isinstance(error, commands.CommandInvokeError):
        # Bad Argument
        if 'target parameter' in str(error):
            embed = discord.Embed(description='{0} Please tag the user you wish to kick.'.format(ctx.message.author.mention))
            embed.color = discord.Color.red()   
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(description='{0} You are not connected to any voice channel.'.format(ctx.message.author.mention))
            embed.color = discord.Color.red()   
            await ctx.send(embed=embed)        
    elif isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(description='{0} Please indicate which user you wish to kick.'.format(ctx.message.author.mention))
        embed.color = discord.Color.red()   
        await ctx.send(embed=embed)

@bot.command()
async def claim(ctx):
    if ctx.message.channel.name != 'command-logs':
        log = discord.utils.get(ctx.message.guild.channels, name='solo-leaderboard')
        eembed = errorembed(description='**{0} Command can only be used in {1}**'.format(userMention, log.mention))
        return await ctx.send(embed=eembed)
    else:     
        channel = ctx.message.author.voice.channel
        for x in channel.members:
            if x.permissions_in(channel).manage_channels is True:
                embed = discord.Embed(description='{0} The original voice channel owner {1} is still present.'.format(ctx.message.author.mention, channel.members[-0].mention))
                embed.color = discord.Color.red()   
                return await ctx.send(embed=embed)
            else:
                overwrite = discord.PermissionOverwrite(manage_channels=True, mute_members=True, deafen_members=True, connect=True, speak=True)
                await channel.set_permissions(ctx.message.author,overwrite=overwrite) 
                embed = discord.Embed(description='{0} You have successfully claimed the voice channel.'.format(ctx.message.author.mention))
                embed.color = discord.Color.green()
                return await ctx.send(embed=embed)
    

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(name='Custom Channels', type=2))
    time_now = datetime.now(tz=pytz.timezone('Asia/Singapore'))
    login_time = time_now.strftime('%d-%m-%Y %I:%M %p')
    print("-----------------")
    print('Logged in as {0} at {1}'.format(bot.user.name, login_time))
    print("-----------------")




bot.run(os.environ.get('BOT_TOKEN'))
    
