import os
import discord
import aiohttp
import pyfiglet
import random
import json
import io
import re
import contextlib
import textwrap
from discord import user
from requests import PreparedRequest
import session
import requests
import datetime
import asyncio
from discord.ext.commands import CommandNotFound
import keep_alive
from itertools import cycle
from discord.utils import get
from discord.ext import commands, tasks
from discord.ext.commands.core import has_permissions
from discord.ext.commands import has_permissions,  CheckFailure, check
import time
import aiofiles
from discord_buttons_plugin import *
from colorama import Fore

bot = commands.Bot(command_prefix="m+")
bot.remove_command("help")
intents= discord.Intents.default()
intents.members = True
prefix = "m+"
bot.sniped_messages = {}
global raid
raid = True

servers = len(bot.guilds)
members = 0
for guild in bot.guilds:
    members += guild.member_count - 1

#Command 1: Help
@bot.command()
async def help(ctx):
  author = ctx.author
  memberAvatar = author.avatar_url
  em = discord.Embed(title = "Meow-bot's help command !", description = "m+help for more details.")
  em.add_field(name = "Fun", value = f"🎰 m+fun for more details.")
  em.add_field(name = "Moderation", value = "<:TCC_blurpleemployee:917337948062642176> m+mod for more details.")
  em.add_field(name = "Utility", value = " <:TCC_blurplegift:917337948167471115> m+utility for more details.")
  em.add_field(name = "NSFW", value = "🔞 m+nsfw for more details.")
  em.add_field(name = "Giveaway", value = "m+gaws for more details.")
  em.set_thumbnail(url=memberAvatar)
  em.set_image(url = 'https://media.giphy.com/media/EOHqVt2BTTvCU/giphy.gif')
  await ctx.send(embed = em)

@bot.command()
async def mod(ctx):
  aki = discord.Embed(title = "Moderation Module !", description = "Meow-bot's moderation commands",  colour = ctx.author.colour)
  aki.add_field(name = "MOD", value = "snipe, clear, nuke, mute, unmute, ban, unban, warn, warnings, kick botinfo, role, membercount")
  await ctx.send(embed=aki)

@bot.command()
async def fun(ctx):
  em = discord.Embed(title = "Fun Module !", description = "Meow-bot's fun commands !", colour = ctx.author.colour)
  em.add_field(name = "FUN", value = "waifu, fbi, neko, coinflip, bang, pat, hug, ble, cry, blush, lick, kiss, slap, kill, wink, punch, smug, poke, bite, dance, wait, meme, gayrate, simprate")
  await ctx.send(embed=em) 

@bot.command()
async def utility(ctx):
  em = discord.Embed(title = "Utility Module !", description = "Meow-bot's utility commands !", colour = ctx.author.colour)
  em.add_field(name = "UTILITY", value = "av, serverinfo, whois, quotes, ascii, ping, rd, invite")
  await ctx.reply(embed=em)

@bot.command()
async def nsfw(ctx):
  em = discord.Embed(title="NSFW !",
  description= "Meow-bot's nsfw commands!",
  color = 0xffff)
  em.add_field(name="Onii-chan hentai:", value="porn - hentai - hneko - blowjob - fuck - loli - bb")
  await ctx.reply(embed=em)

@bot.command()
async def gaws(ctx):
  aki = discord.Embed(title = "Giveaway Module !", description = "Meow-bot's giveaway commands",  colour = ctx.author.colour)
  aki.add_field(name = "Gaws", value = "gstart")
  await ctx.send(embed=aki)

#============================
  #moderation commands:
@bot.event
async def on_message_delete(message):
	bot.sniped_messages[message.guild.id] = (message.content, message.author, message.channel.name,
message.created_at)


@bot.command()
async def snipe(ctx):
	try:
		contents, author, channel_name, time = bot.sniped_messages[
		    ctx.guild.id]

	except:
		await ctx.channel.send("I couldn't find message to snipe!")
		return

	embed = discord.Embed(description=contents,
	                      color=discord.Color.purple(),
	                      timestamp=time)
	embed.set_author(name=f"{author.name}#{author.discriminator}",
	                 icon_url=author.avatar_url)
	embed.set_footer(text=f"Deleted in : #{channel_name}")

	await ctx.channel.send(embed=embed)

@bot.command()
async def ping(ctx):
	before = time.monotonic()
	msg = await ctx.send("Pong!")
	ping = (time.monotonic() - before) * 1000.
	await msg.edit(content=f"Pong! `{int(ping)}ms`")

@bot.command(aliases=["purge"])
@commands.has_permissions(manage_channels=True)
async def clear(ctx, amount=0):
  await ctx.channel.purge(limit = amount + 1)

@bot.command()
@commands.has_permissions(administrator=True)
async def nuke(ctx, channel: discord.TextChannel = None):
    if channel == None: 
        await ctx.send("You have to mention a channel!")
        return

    nuke_channel = discord.utils.get(ctx.guild.channels, name=channel.name)

    if nuke_channel is not None:
        new_channel = await nuke_channel.clone(reason="Nuked successfully!")
        await nuke_channel.delete()
        await new_channel.send(f"This channel has been nuked by {ctx.author.mention}")
        await ctx.send("Nuked successfully!")

    else:
        await ctx.send(f"No channel named {channel.name} has been found!")
      
@bot.command(name='membercount')
async def membercount(ctx):
  memberCount = str(ctx.guild.member_count)

  embed= discord.Embed(title=f"Members at {ctx.guild.name}", description=f"{memberCount} members", color = 0xffff)
  embed.set_footer(text=f"Requested by {ctx.author}")
  await ctx.send(embed=embed)

@bot.command()
@commands.has_permissions(kick_members=True)
async def mute(ctx, member: discord.Member, *, reason=None):
	guild = ctx.guild
	mutedRole = discord.utils.get(guild.roles, name="Muted")

	if not mutedRole:
		mutedRole = await guild.create_role(name="Muted")

		for channel in guild.channels:
			await channel.set_permissions(mutedRole,
			                              speak=False,
			                              send_messages=False,
			                              read_message_history=True,
			                              read_messages=False)
	embed = discord.Embed(title="Muted",
	                      description=f"{member.mention} has been muted",
	                      colour=discord.Colour.light_gray())
	embed.add_field(name="Reason:", value=reason, inline=False)
	await ctx.send(embed=embed)
	await member.add_roles(mutedRole, reason=reason)
	await member.send(
	    f"You have been muted in **{guild.name}** because of : **{reason}**")

@bot.command()
@commands.has_permissions(kick_members=True)
async def unmute(ctx, member: discord.Member):
	mutedRole = discord.utils.get(ctx.guild.roles, name="Muted")

	await member.remove_roles(mutedRole)
	embed = discord.Embed(title="Unmuted",
	                      description=f"{member.mention} has been unmuted !",
	                      colour=discord.Colour.light_gray())
	await ctx.send(embed=embed)

@bot.command()
@commands.has_permissions(manage_channels=True)
async def lock(ctx, channel : discord.TextChannel=None):
    channel = channel or ctx.channel
    overwrite = channel.overwrites_for(ctx.guild.default_role)
    overwrite.send_messages = False
    await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
    await ctx.send(f'This channel has been locked by {ctx.author.mention}')

@bot.command()
@has_permissions(manage_channels=True)
async def unlock(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
    await ctx.send(ctx.channel.mention + f" **has been unlocked by: {ctx.author.mention}**")

@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
	try:
		await member.ban(reason=reason)
		await ctx.send(f'Banned {member.mention}')
	except:
		await ctx.send(f'I counld not ban {member.mention}')

@ban.error
async def ban_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please enter a reason/user to ban!")

@bot.command(name='unban')
@commands.has_permissions(ban_members=True)
async def unban(ctx, id: int):
    user = await bot.fetch_user(id)
    await ctx.channel.send(f'{user.mention} has been unbanned!')
    await ctx.guild.unban(user)

@unban.error
async def unban_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please enter a user id you want to unban!")

def is_it_me(ctx):
  return ctx.author.id == ctx.author.id

bot.warnings = {} 

@bot.event
async def on_ready():
	for guild in bott.guilds:
		bot.warnings[guild.id] = {}

		async with aiofiles.open(f"{guild.id}.txt", mode="a") as temp:
			pass

		async with aiofiles.open(f"{guild.id}.txt", mode="r") as file:
			lines = await file.readlines()

			for line in lines:
				data = line.split(" ")
				member_id = int(data[0])
				admin_id = int(data[1])
				reason = " ".join(data[2:]).strip("\n")

				try:
					bot.warnings[guild.id][member_id][0] += 1
					bot.warnings[guild.id][member_id][1].append(
					    (admin_id, reason))

				except KeyError:
					bot.warnings[guild.id][member_id] = [
					    1, [(admin_id, reason)]
					]


@bot.event
async def on_guild_join(guild):
	bot.warnings[guild.id] = {}

def owner(ctx):
  return ctx.author.id == 926777498312798258

@bot.command()
@commands.has_permissions(kick_members=True)
async def warn(ctx, member: discord.Member = None, *, reason=None):
	if member is None:
		return await ctx.send(
		    "Couldn't find the user you wanted to warn!"
		)

	if reason is None:
		return await ctx.send("Please enter a reason to warn this user.")

	try:
		first_warning = False
		bot.warnings[ctx.guild.id][member.id][0] += 1
		bot.warnings[ctx.guild.id][member.id][1].append(
		    (ctx.author.id, reason))

	except KeyError:
		first_warning = True
		bot.warnings[ctx.guild.id][member.id] = [1, [(ctx.author.id, reason)]]

	count = bot.warnings[ctx.guild.id][member.id][0]

	async with aiofiles.open(f"{ctx.guild.id}.txt", mode="a") as file:
		await file.write(f"{member.id} {ctx.author.id} {reason}\n")

	await ctx.send(
	    f"{member.mention} has {count} {'warnings' if first_warning else 'warnings'}."
	)

@bot.command()
@commands.has_permissions(manage_messages=True)
async def warnings(ctx, member: discord.Member = None):
	if member is None:
		return await ctx.send(
		    "Couldn't find the user you want to see warningss"
		)

	embed = discord.Embed(title=f"Warnings of {member.name}",
	                      description="",
	                      colour=discord.Colour.red())
	try:
		i = 1
		for admin_id, reason in bot.warnings[ctx.guild.id][member.id][1]:
			admin = ctx.guild.get_member(admin_id)
			embed.description += f"**Warned {i}** by: {admin.mention} because: *'{reason}'*.\n"
			i += 1

		await ctx.send(embed=embed)

	except KeyError:  # no warnings
		await ctx.send("This user has no warnings.")

@bot.command()
@commands.has_permissions(kick_members = True)
async def kick(ctx, member: discord.Member, *, reason=None):
	try:
		await member.kick(reason=None)
		await ctx.send(f'{member} has been kicked')
	except:
		await ctx.send("Couldn't kick that user")

def convert(time):
  pos = ["s","m","h","d"]

  time_dict = {"s" : 1, "m" : 60, "h" : 3600, "d": 3600*24}

  unit = time[-1]
  
  if unit not in pos:
    return -1
  try:
    val = int(time[:-1])
  except:
    return -2

  return val * time_dict[unit]

#Utility commands  
def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return(quote)

@bot.command()
async def quotes(ctx):
  quote = get_quote()
  await ctx.send(quote)
  
@bot.command()
async def avatar(ctx, member: discord.Member = None):
	if member == None:
		member = ctx.author

	memberAvatar = member.avatar_url

	avaEmbed = discord.Embed(title=f"{member.name}'s avatar")
	avaEmbed.set_image(url=memberAvatar)
	await ctx.send(embed=avaEmbed)


@bot.command(pass_context = True)
async def setnick(ctx, member: discord.Member, nick):
   await member.edit(nick = nick)
   await ctx.send(f'Nickname set for {member.mention}')

format = "%a, %d %b %Y | %H:%M:%S %ZGMT"

@bot.command(aliases=['svi'])
@commands.guild_only()
async def serverinfo(ctx):
    embed = discord.Embed(
        color = ctx.author.color
    )
    text_channels = len(ctx.guild.text_channels)
    voice_channels = len(ctx.guild.voice_channels)
    categories = len(ctx.guild.categories)
    channels = text_channels + voice_channels
    embed.set_thumbnail(url = str(ctx.guild.icon_url))
    embed.add_field(name = f"Info about **{ctx.guild.name}**: ", value = f":white_small_square: ID: **{ctx.guild.id}** \n:white_small_square: Owner: **{ctx.guild.owner}**  \n:white_small_square: Created date: **{ctx.guild.created_at.strftime(format)}** \n:white_small_square: Members: **{ctx.guild.member_count}** \n:white_small_square: Channels: **{channels}** channels; **{text_channels}** Text channels, **{voice_channels}** voice channels, **{categories}** categories \n:white_small_square: Security: **{str(ctx.guild.verification_level).upper()}** \n:white_small_square: Info: {', '.join(f'**{x}**' for x in ctx.guild.features)} \n:white_small_square: Splash: {ctx.guild.splash}")
    await ctx.send(embed=embed)


@bot.command('role')
@commands.has_permissions(manage_roles=True)
async def role(ctx, user : discord.Member, *, role : discord.Role):
  if role.position > ctx.author.top_role.position:
    return await ctx.send('**❌ | That role is higher than your highest role!**') 
  if role in user.roles:
      await user.remove_roles(role)
      await ctx.send(f"Removed {role} from {user.mention}")
  else:
      await user.add_roles(role)
      await ctx.send(f"Added {role} for {user.mention}")

@bot.command(aliases=["whois"])
async def userinfo(ctx, member: discord.Member = None):
    if not member:  
        member = ctx.message.author  
    roles = [role for role in member.roles]
    embed = discord.Embed(colour=discord.Colour.purple(), timestamp=ctx.message.created_at,
                          title=f"User Info - {member}")
    embed.set_thumbnail(url=member.avatar_url)
    embed.set_footer(text=f"Requested by {ctx.author}")

    embed.add_field(name="ID:", value=member.id)
    embed.add_field(name="Name:", value=member.display_name)

    embed.add_field(name="Created date:", value=member.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"))
    embed.add_field(name="Joined at :", value=member.joined_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"))

    embed.add_field(name="Roles:", value="".join([role.mention for role in roles]))
    embed.add_field(name="Highest role:", value=member.top_role.mention)
    print(member.top_role.mention)
    await ctx.send(embed=embed)
    
@bot.command()
async def invite(ctx):
	await ctx.send(
	    "https://discord.com/api/oauth2/authorize?client_id=924858871380594729&permissions=8&scope=bot")

@bot.command()
async def rd(ctx, *, args=None):
	if args == None:
		rd = random.randint(1, 100)
		await ctx.send("🎲 The random number is: " + str(rd))
	else:
		rd2 = random.randint(1, int(args))
		await ctx.send("🎲 The random number is: " + str(rd2))

@bot.command()
async def say(ctx, *, text):
# Ngăn chặn ping everyone
  if "@everyone" in text or "@here" in text or "@" in text:
    await ctx.send("Bạn không thể ping everyone/here! <a:TCC_lmao3:920721616126754897> ||Bach Wumpus fixes that lol!|| https://cdn.discordapp.com/attachments/941963443471274055/944526764250652692/unknown.png")
    return
    # - Bach Wumpus
  message = ctx.message
  await message.delete()

  await ctx.send(f"{text}")

@bot.event
async def on_ready():
	print(Fore.YELLOW + f"""
               ___              ___
              |   \            /   |
              |    \          /    |
              |     \        /     |
              |      \      /      |
              |       \    /       |
              |        \  /        |
              |         \/         |
              |   |\          /|   |
              |   | \        / |   |
              |   |  \      /  |   |
              |___|   \____/   |___|

 """)
	print('Logged in as:\n{0.user.name}\n{0.user.id}'.format(bot))
	print(Fore.MAGENTA + f"----------------")
	print(Fore.LIGHTBLUE_EX + f"Meow-san's cool bot")
	print(Fore.LIGHTGREEN_EX + f"----------------")
	print(Fore.RED + f"Enjoy using UwU")
	print(Fore.LIGHTBLUE_EX + f"----------------")
	await bot.change_presence(activity=discord.Game(name="Chơi cùng  Meow-san")
	                          )

#Fun Command=========
@bot.command()
@commands.guild_only()
async def waifu(ctx):
    r = requests.get("https://api.waifu.pics/sfw/waifu")
    r = r.json()
    ulr = r['url']
    embed=discord.Embed(title=f"Here's your wifu")
    embed.set_image(url=ulr)
    await ctx.send(embed=embed)

@bot.command(name="neko")
@commands.guild_only()
async def neko(ctx):
    q = [f"https://api.waifu.pics/sfw/neko"]
    s = random.choice(q)
    r = requests.get(s)
    r = r.json()
    ulr = r['url']
    embed=discord.Embed(title=f"Here's your neko")
    embed.set_image(url=ulr)
    await ctx.send(embed=embed)
    
@bot.command()
async def coinflip(ctx):
  choicezz = ['Heads!', 'Tails!']
  await ctx.send("The coin flipped and it's " + random.choice(choicezz))

@bot.command()
async def bang(ctx):
   em = discord.Embed(title=f"{ctx.author} đã bắn không khí", color=0xffff)
   em.set_image(url="https://cdn.discordapp.com/attachments/927713935044513804/927819171629252659/anime-loli.gif")
   await ctx.reply(embed=em)

@bot.command()
async def pat(ctx, user_1 : discord.Member=None, user_2 : discord.Member=discord.Member):
  if not user_1 == None:
    if user_2 == None:
      user = ctx.author
      users = user_1
    if not user_2 == None:
      user = user_1
      users = user_2
    r = requests.get("https://api.waifu.pics/sfw/pat")
    r = r.json()
    ulr = r['url']
    embed=discord.Embed(title=f"{ctx.author} patted {user_1}", color = 0xffff)
    embed.set_image(url=ulr)
    await ctx.reply(embed=embed)

@bot.command()
async def hug(ctx, user_1 : discord.Member=None, user_2 : discord.Member=discord.Member):
  if not user_1 == None:
    if user_2 == None:
      user = ctx.author
      users = user_1
    if not user_2 == None:
      user = user_1
      users = user_2
    r = requests.get("https://api.waifu.pics/sfw/hug")
    r = r.json()
    ulr = r['url']
    embed=discord.Embed(title=f"{user_1} has been hugged by {ctx.author}", color = 0xffff)
    embed.set_image(url=ulr)
    await ctx.reply(embed=embed)

@bot.command()
async def ble(ctx):
  em = discord.Embed(title="Ble", color=0xffff)
  em.set_image(url="https://media.discordapp.net/attachments/927713935044513804/927776209977376798/Frog_Tongue_Out_Sticker_-_Frog_Tongue_Out_Teasing_-_Discover__Share_GIFs.gif?width=431&height=431")
  await ctx.reply(embed=em)

@bot.command()
async def cry(ctx):
    r = requests.get("https://api.waifu.pics/sfw/cry")
    r = r.json()
    ulr = r['url']
    embed=discord.Embed(title=f"{ctx.author} is crying!", color = 0xffff)
    embed.set_image(url=ulr)
    await ctx.reply(embed=embed)

@bot.command()
async def blush(ctx):
  r = requests.get("https://api.waifu.pics/sfw/blush")
  r = r.json()
  ulr = r['url']
  embed = discord.Embed(title=f"{ctx.author} is blushing", color = 0xffff)
  embed.set_image(url=ulr)
  await ctx.reply(embed=embed)

@bot.command()
async def lick(ctx, user_1 : discord.Member=None, user_2 : discord.Member=discord.Member):
  if not user_1 == None:
    if user_2 == None:
      user = ctx.author
      users = user_1
    if not user_2 == None:
      user = user_1
      users = user_2

    r = requests.get("https://api.waifu.pics/sfw/lick")
    r = r.json()
    ulr = r['url']
    embed=discord.Embed(title=f"{user_1} has been licked by {ctx.author}", color = 0xffff)
    embed.set_image(url=ulr)
    await ctx.reply(embed=embed)

@bot.command()
async def kiss(ctx, user_1 : discord.Member=None, user_2 : discord.Member=discord.Member):
  if not user_1 == None:
    if user_2 == None:
      user = ctx.author
      users = user_1
    if not user_2 == None:
      user = user_1
      users = user_2

    r = requests.get("https://api.waifu.pics/sfw/kiss")
    r = r.json()
    ulr = r['url']
    embed=discord.Embed(title=f"{user_1} has been kissed by {ctx.author}", color = 0xffff)
    embed.set_image(url=ulr)
    await ctx.reply(embed=embed)

@bot.command()
async def slap(ctx, user_1 : discord.Member=None, user_2 : discord.Member=discord.Member):
  if not user_1 == None:
    if user_2 == None:
      user = ctx.author
      users = user_1
    if not user_2 == None:
      user = user_1
      users = user_2

    r = requests.get("https://api.waifu.pics/sfw/slap")
    r = r.json()
    ulr = r['url']
    embed=discord.Embed(title=f"{user_1} has been slapped by {ctx.author}", color = 0xffff)
    embed.set_image(url=ulr)
    await ctx.reply(embed=embed)

@bot.command()
async def kill(ctx, user_1 : discord.Member=None, user_2 : discord.Member=discord.Member):
  if not user_1 == None:
    if user_2 == None:
      user = ctx.author
      users = user_1

    if not user_2 == None:
      user = user_1
      users = user_2

    r = requests.get("https://api.waifu.pics/sfw/kill")
    r = r.json()
    ulr = r['url']
    aki=discord.Embed(title=f"{ctx.author} killed {user_1} !")
    aki.set_image(url=ulr)
    await ctx.reply(embed=aki)

@bot.command()
async def wink(ctx):
#quên
    r = requests.get("https://api.waifu.pics/sfw/wink")
    r = r.json()
    ulr = r['url']
    aki=discord.Embed(title=f"{ctx.author} is winking", color=0xffff)
    aki.set_image(url=ulr)
    await ctx.reply(embed=aki)

@bot.command()
async def punch(ctx, user_1 : discord.Member=None, user_2 : discord.Member=discord.Member):
  if not user_1 == None:
    if user_2 == None:
      user = ctx.author
      users = user_1
    if not user_2 == None:

     r = requests.get("https://api.waifu.pics/sfw/bully")
     r = r.json()
     ulr = r['url']
     kimi = discord.Embed(title=f"{user_1} has been punched by {ctx.author}", color = 0xffff)
     kimi.set_image(url=ulr)
     await ctx.reply(embed=kimi)

@bot.command()
async def smug(ctx):
    r = requests.get("https://api.waifu.pics/sfw/smug")
    r = r.json()
    ulr = r['url']
    embed=discord.Embed(title=f"{ctx.author} is smugging", color = 0xffff)
    embed.set_image(url=ulr)
    embed.set_footer(text="By AKM coding")
    await ctx.reply(embed=embed)

@bot.command()
async def poke(ctx, user_1 : discord.Member=None, user_2 : discord.Member=discord.Member):
  if not user_1 == None:
    if user_2 == None:
      user = ctx.author
      users = user_1
    if not user_2 == None:
      user = user_1
      users = user_2
  r = requests.get("https://api.waifu.pics/sfw/poke")
  r = r.json()
  ulr = r['url']
  embed = discord.Embed(title=f"{ctx.author} is poking {user_1}!")
  embed.set_image(url=ulr)
  await ctx.reply(embed=embed)

@bot.command()
async def bite(ctx, user_1 : discord.Member=None, user_2 : discord.Member=discord.Member):
  if not user_1 == None:
    if user_2 == None:
      user = ctx.author
      users = user_1
    if not user_2 == None:
      user = user_1
      users = user_2

  r = requests.get("https://api.waifu.pics/sfw/bite")
  r = r.json()
  ulr = r['url']
  embed = discord.Embed(title=f"{ctx.author} is biting {user_1}")
  embed.set_image(url=ulr)
  await ctx.reply(embed=embed)



@bot.command()
async def dance(ctx):

  r = requests.get("https://api.waifu.pics/sfw/dance")
  r = r.json()
  ulr = r['url']
  em = discord.Embed(title=f"{ctx.author} is dancing", color=0xffff)
  em.set_image(url=ulr)
  await ctx.reply(embed=em)

@bot.command()
async def wait(ctx):
  em = discord.Embed(title=f"{ctx.author} is waiting for something", color=0xffff)
  em.set_image(url="https://cdn.discordapp.com/attachments/921395702721040415/927838296128757800/loli-anime.gif")
  await ctx.reply(embed=em)

@bot.command(pass_context=True)
async def meme(ctx):
    cak = discord.Embed(title="Here's ur meme!", color=0xffff)

    async with aiohttp.ClientSession() as cs:
        async with cs.get('https://www.reddit.com/r/dankmemes/new.json?sort=hot') as r:
            res = await r.json()
            cak.set_image(url=res['data']['children'] [random.randint(0, 25)]['data']['url'])
            await ctx.send(embed=cak)

@bot.command()
async def gayrate(ctx, member: discord.Member = None):
	gay = random.randint(1, 100)
	if member == None:
		gayrate = ctx.author
		embed = discord.Embed(title="Gay-rate Machine",
		                      description=f"{gayrate} is gay {gay}%")
	else:
		embed = discord.Embed(title="Gay-rate Machine",
		                      description=f"{member.mention} is gay {gay}% ")
	await ctx.send(embed=embed)

@bot.command()
async def simprate(ctx, member: discord.Member = None):
	simp = random.randint(1, 100)
	if member == None:
		simprate = ctx.author
		embed = discord.Embed(title="Simp-rate Machine",
		                      description=f"{simprate} is simp {simp}%")
	else:
		embed = discord.Embed(title="Simp-rate Machine",
		                      description=f"{member.mention} is simp {simp}%")
	await ctx.send(embed=embed)


@bot.command()
@commands.guild_only()
async def ship(ctx, user_1 : discord.Member=None, user_2 : discord.Member=None):
  if not user_1 == None:
    if user_2 == None:
      user = ctx.author
      users = user_1
    if not user_2 == None:
      user = user_1
      users = user_2
    arg = random.randint(1, 100)   
    r = requests.get("https://api.waifu.pics/sfw/hug")
    r = r.json()
    ulr = r['url']

    embed = discord.Embed(title=f"The love from {user} for {users} is {arg}% ❤️")
    embed.set_image(url=ulr)

    await ctx.channel.send(embed=embed)
  if users == None:
    users = ctx.author

# Listing Blacklist user:
blacklist = ['703810425505972286', '926709117844869150', '894120820702605334', '876665254002688070', '752848869452414997', '707582914904326195', '939831606653354024']

@bot.command()
async def spam(ctx, *, message):
  global raid
  # Blacklist user
  if str(ctx.author.id) in blacklist:
    await ctx.send("Bạn đã bị ban sử dụng lệnh spam! Nếu bạn muốn unban vui lòng liên hệ Bach Wumpus và Meow-chan")
    return
  # Ngăn chặn ping everyone
  elif "@everyone" in message or "@here" in message or "@" in message:
    await ctx.send("Bạn không thể ping everyone/here/roles/user! <a:TCC_lmao3:920721616126754897> ||Bach Wumpus fixes that lol!|| https://cdn.discordapp.com/attachments/941963443471274055/944526764250652692/unknown.png")
    return
    # - Bach Wumpus
  raid = True
  while raid:
    await ctx.send(message)
  

@bot.command()
async def stop(ctx):
	global raid
	raid = False

@bot.command()
async def spamcheck(ctx):
  if str(ctx.author.id) in blacklist:
    await ctx.send("Bạn đã bị blacklist sử dụng lệnh spam! Nếu bạn muốn unban vui lòng liên hệ Bach Wumpus và Meow-chan")
    return
  await ctx.send("Bạn không bị blacklist!")



@bot.command()
async def spamping(ctx, *, message):
  global raid
  whitelistspamping = ['624091967625625610', '901035097602523137']
  if ctx.author.id in whitelistspamping:
    raid = True
    while raid:
     await ctx.send(message)


#########
#gaws command #gaws = giveaways

time_regex = re.compile(r"(?:(\d{1,5})(h|s|m|d))+?")
time_dict = {"h": 3600, "s": 1, "m": 60, "d": 86400}

def convert(argument):
    args = argument.lower()
    matches = re.findall(time_regex, args)
    time = 0
    for key, value in matches:
        try:
            time += time_dict[value] * float(key)
        except KeyError:
            raise commands.BadArgument(
                f"{value} Need to be a valid time !For example : 10s|10m|10h|10d"
            )
        except ValueError:
            raise commands.BadArgument(f"{key} is invalid")
    return round(time)

@bot.command()
@commands.has_permissions(manage_messages=True)
async def gstart(ctx, timing, winners: int, *, prize):
  await ctx.send('Giveaway has started!', delete_after=3)
  gwembed = discord.Embed(
    title="🎉 __**Giveaway**__ 🎉",
    description=f'**{prize}**',
    color=0xb4e0fc
  )
  gwembed.add_field(name="React ✅ to join !", value="React !!! ✅")
  time = convert(timing)
  gwembed.set_footer(text=f"Ended in {time} secs | started by {ctx.author}")
  gwembed = await ctx.send(embed=gwembed)
  await gwembed.add_reaction("✅")
  await asyncio.sleep(time)
  message = await ctx.fetch_message(gwembed.id)
  users = await message.reactions[0].users().flatten()
  users.pop(users.index(ctx.guild.me))
  if len(users) == 0:
    await ctx.send("There's no winner.")
    return
  for i in range(winners):
    winner = random.choice(users)
    await ctx.send(f"Congrats {winner.mention} has winned **{prize}** started by {ctx.author.mention}!")

#=============
#NFSW COMMAND
@bot.command()
@commands.is_nsfw()
async def porn(ctx):
  embed = discord.Embed(title="Porn", color=0xffff)
  async with aiohttp.ClientSession() as cs:
    async with cs.get('https://www.reddit.com/r/nsfw/new.json?sort=hot') as r:
      res = await r.json()
      embed.set_image(url=res['data']['children'] [random.randint(0, 25)]['data']['url'])
      await ctx.send(embed=embed)

@porn.error
async def porn_error(ctx, error):
    if isinstance(error, commands.NSFWChannelRequired):
        await ctx.send(f"Hey {ctx.author.mention}, you can only use this command in a nsfw channel!")


@bot.command(name="hentai")
@commands.guild_only()
@commands.is_nsfw()
async def hentai(ctx):
    q = ["https://api.waifu.pics/nsfw/waifu"]
    s = random.choice(q)
    r = requests.get(s)
    r = r.json()
    ulr = r['url']
    embed=discord.Embed(title=f"Here's ur hentai")
    embed.set_image(url=ulr)
    await ctx.send(embed=embed)

@hentai.error
async def hentai_error(ctx, error):
    if isinstance(error, commands.NSFWChannelRequired):
        await ctx.send(f"Hey {ctx.author.mention}, you can only use this command in a nsfw channel!")


@bot.command()
@commands.is_nsfw()
async def bb(ctx):
  cak = ['https://images-ext-1.discordapp.net/external/r3iQdb20SIz3Bt_OZmVm8la_bfQCng850mOOELyPhQg/https/cdn.zerotwo.dev/BOOBS/101060b7-1fb4-4303-818f-b96f938ae26e.gif','https://images-ext-2.discordapp.net/external/tzYuHy11B1IIG5S-wAw6X5cyYoQ0zvKKa8rSKL9oah8/https/cdn.zerotwo.dev/BOOBS/b9e58412-02db-4586-8cfe-848b2150e11b.gif?width=651&height=431',
'https://images-ext-2.discordapp.net/external/OdYrOcaPWOZxV4WUuhuZ-AZSlbJsgGHzLfNJb1bHZag/https/cdn.zerotwo.dev/BOOBS/d7b2f21c-3d1b-4bd3-8d8d-401c1a3088f7.gif',
'https://images-ext-1.discordapp.net/external/nbGGV8KCBX7hC2DrWYfswE8lbqdiDC7L1GRcZgcgjOY/https/cdn.zerotwo.dev/BOOBS/14425806-f183-43c7-bd5c-a12cfb0c2b2a.gif',
'https://images-ext-1.discordapp.net/external/5J_IdUpSaZhr8sp2f37uPVRsj1V2xrmDA1HJDNMLmJ4/https/cdn.zerotwo.dev/BOOBS/107a20be-c5b6-44ea-9a96-f6cf68b5a9d7.gif',
'https://images-ext-1.discordapp.net/external/exjVlqO2a_Bc9OS7RQIe6sJgRMqS-XazqUv3IHHThms/https/cdn.zerotwo.dev/BOOBS/50b58ab6-7608-4d33-93b7-ff0651713142.gif']
  embed = discord.Embed(title="Boobs lol!!!", color=0xffff)
  embed.set_image(url=f"{random.choice(cak)}")
  
  await ctx.send(embed=embed)

@bb.error
async def bb_error(ctx, error):
    if isinstance(error, commands.NSFWChannelRequired):
        await ctx.send(f"Hey {ctx.author.mention}, you can only use this command in a nsfw channel!")

@bot.command(aliases=['codehentai'])
@commands.is_nsfw()
async def nhentai(ctx):
  code = ["167466", "165684", "254048", "175015", "174016", "142825", "129128", "171417", "129128", "95809", "239567", "247021", "46579", "123580", "171417", "173543", "197422", "187835", "217832", "206573", "169546", "193107", "190805", "220309", "211112", "132768", "97945", "164783", "206446", "251608", "90182", "256018", "138470", "110826", "175494", "134764", "145647", "212562", "179166", "214784", "176977", "191434", "191434", "239536", "236342", "227702", "204425", "205079", "85333", "232837", "232385", "232341", "254087", "50535", "235202", "94159", "52365", "255034", "153045", "159457", "173235", "96270", "196020", "191774", "230332", "95298", "89514", "73649", "203027", "217404", "65573", "255457", "199874", "233133", "205367" "233693", "50046", "234191", "209455", "206366", "253799", "39249", "172197", "243552", "223998", "221050", "217456", "225019", "234165", "258245", "247696", "258212", "258465", "86493", "258133", "244327", "260640", "261171", "244996", "202634", "165950", "220967", "120977", "204746", "142850", "99439", "232439" , "246032", "200948", "265804", "25913", "262861", "196077", "155489", "257528", "267270", "177044", "267502", "184840", "144714", "228575", "268002", "267980", "227439", "267980", "268015", "89502", "228575" , "220893", "160609", "261107", "110747", "235532", "248196", "228948", "259361", "235032", "139512", "257528", "260369", "261650", "234174", "116174", "249554", "249551", "249543", "49544", "166427", "206295", "168574", "249497", "72987", "181008", "242987", "251019", "251008", "251007", "185572", "69431", "187626", "251014", "251015", "251027", "251028", "251029", "251024", "251026", "239732",  "213835", "146913", "216227", "182290", "117013", "259600", "139512", "258479", "173101", "235532", "258488", "264551", "263661", "242668", "154884", "150096", "265842", "259137", "781573", "234734", "244436", "265841", "265837", "255337", "110955", "265842", "266301", "928040", "122557", "135420", "209519", "265756", "136489", "242517", "266965", "134035", "266613", "183469", "244996", "255662", "267352", "267270", "267043", "213560", "261868", "267352", "186938", "267369", "263516", "266942", "111292", "233513", "262069", "172807", "263960", "184840", "266495", "252548", "267617", "193770", "262668", "225918", "147759", "154290", "240108", "240110", "208486", "240113", "257960", "109168", "109395", "109519", "112206", "231215", "246186", "267980", "259491", "265933", "196016", "235032", "228948", "131056", "121927", "134861", "195791", "116300", "268362", "152889", "134500", "268338", "220735", "192060", "113276", "265526", "264824", "126784", "191851", "103366", "229144", "158651", "257484", "248696", "265804", "206387", "158123", "136188", "235928", "194941", "208797", "241819", "239732", "215376", "220212", "165957", "266906", "268529", "267352","229144", "253687", "238577",]

  await ctx.send(f"Here's your code {random.choice(code)}")

@bot.command(name="hneko")
@commands.guild_only()
@commands.is_nsfw()
async def hneko(ctx):
    q = ["https://api.waifu.pics/nsfw/neko"]
    s = random.choice(q)
    r = requests.get(s)
    r = r.json()
    ulr = r['url']
    embed=discord.Embed(title="Here's ur neko")
    embed.set_image(url=ulr)
    await ctx.send(embed=embed)

@hneko.error
async def hneko_error(ctx, error):
    if isinstance(error, commands.NSFWChannelRequired):
        await ctx.reply(f"Hey {ctx.author.mention}, you can only use this command in a nsfw channel!")

@bot.command()
@commands.is_nsfw()
async def fuck(ctx, user_1 : discord.Member=None, user_2 : discord.Member=discord.Member):
  if not user_1 == None:
    if user_2 == None:
      user = ctx.author
      users = user_1
    if not user_2 == None:
      user = user_1
      users = user_2
    choicesss = ['https://cdn.discordapp.com/attachments/736281485216317442/736281794927919164/fuck.gif', 'https://cdn.discordapp.com/attachments/736281485216317442/736281509488754740/fuck.gif', 'https://cdn.sex.com/images/pinporn/2013/07/21/3238759.gif?width=620', 'https://images-ext-1.discordapp.net/external/NOpUdEv4ojFdpQPfB-yOijj_DZ59LKe6yU2QcFpbzMM/http/xxxpicz.com/xxx/gifs-hentai-porno-hentai-vidahentaiporn-1.gif?width=400&height=234']

    embed=discord.Embed(title=f"{ctx.author} is fucking {user_1} :o")
    embed.set_image(url=f"{random.choice(choicesss)}")
    await ctx.reply(embed=embed)

@fuck.error
async def fuck_error(ctx, error):
    if isinstance(error, commands.NSFWChannelRequired):
      await ctx.reply(f"Hey {ctx.author.mention}, you can only use this command in a nsfw channel!")

@bot.command()
@commands.is_nsfw()
async def loli(ctx):
  embed = discord.Embed(title=f"FBI's here {ctx.author.name}")
  embed.set_image(url="https://cdn.discordapp.com/attachments/932139377159700501/935384522655158332/fbi-open.gif")
  await ctx.reply(embed=embed)

@loli.error
async def loli_error(ctx, error):
  if isinstance(error, commands.NSFWChannelRequired):
    await ctx.send("Oh shit r u watching loli?")

#Error handler
@bot.event
async def on_command_error(ctx, error):
	if isinstance(error, commands.MissingRequiredArgument):
		embed = discord.Embed(
		    title="**__『MISSING ARGUMENT』__**",
		    description=
		    "The argument is missing, add something after the command.",
		    color=0x000000)
		await ctx.send(embed=embed)
	if isinstance(error, commands.MissingPermissions):
		embed1 = discord.Embed(
		    title="**__『MISSING PERMISSIONS』__**",
		    description=
		    "Looks like you're missing the permissions to run this command.",
		    color=0x000000)
		await ctx.send(embed=embed1)
	if isinstance(error, commands.BotMissingPermissions):
		embed4 = discord.Embed(title="**__『MISSING PERMISSIONS』__**",
		                       description="Missing permissions",
		                       color=0x000000)
		await ctx.send(embed=embed4)
	if isinstance(error, CommandNotFound):
		embed = discord.Embed(
		    title="**__『COMMAND NOT FOUND』__**",
		    description=f"\n```\nThe command you runned doesn't exist. \n```\n",
		    color=0x000000)
		await ctx.send(embed=embed)
		return
	raise error

keep_alive.keep_alive()

bot.run (os.environ['token'])