import discord
from app import keep_alive
from discord.ext import commands, tasks
import os
import json
import asyncio

bot = commands.AutoShardedBot(command_prefix = "<")
bot.load_extension("jishaku")

@bot.event
async def on_ready():
  print(f"Discord bot online as {bot.user}")
  update_count.start()
  update_bots.start()
  
@bot.check
async def global_check(ctx):

  r = discord.utils.get(ctx.guild.roles, id = 613656205004636171)

  if r in ctx.author.roles:

    return True
  
  else:

    return False
  
@tasks.loop(seconds=10)
async def update_count():

  online = str(len([x for x in bot.get_guild(611322575674671107).members if x.status == discord.Status.online]))
  dnd = str(len([x for x in bot.get_guild(611322575674671107).members if x.status == discord.Status.dnd]))
  idle = str(len([x for x in bot.get_guild(611322575674671107).members if x.status == discord.Status.idle]))
  offline = str(len([x for x in bot.get_guild(611322575674671107).members if x.status == discord.Status.offline]))
  bots = str(len([x for x in bot.get_guild(611322575674671107).members if x.bot]))

  with open("shit.json", "r") as f:

    l = json.load(f)

  l["online"]=str(online)    
  l["dnd"]=str(dnd)
  l["idle"] = str(idle)
  l["offline"] = str(offline)
  l["bots"] = str(bots)
  
  with open("shit.json", "w+") as f:
    json.dump(l,f,indent=4)

@tasks.loop(seconds = 5)
async def update_bots():

  with open("bots.json", "r") as f:

    l = json.load(f)

  guild = bot.get_guild(611322575674671107)

  for a in guild.members:

    if a.bot:

      if a.activity:

        activity_name = a.activity.name
        activity_type = a.activity.type

      else:

        activity_name = "No Activity"
        activity_type = "No Activity"

      l[str(a)] = {"username": str(a), "name": str(a.name), "id": a.id, "avatar_url": str(a.avatar_url), "activity": {"name": str(activity_name), "type": str(activity_type)}, "status": str(a.status)}

    with open("data/bots.json", "w") as f:
      
      json.dump(l, f, indent = 4)
      
    print("Updated all-bots.json")

@bot.command(hidden = True)
@commands.is_owner()
async def load(self, ctx, extension):
    emb = discord.Embed(title = 'Loading...', colour = discord.Colour.blue())
    emb1 = discord.Embed(title = f'Loaded {extension}!', colour = discord.Colour.green())
    msg = await ctx.send(embed = emb)
    await asyncio.sleep(0.5)
    error = discord.Embed(title = f"""UH! There was an error with {extension}! Check this list:
>>> `The extension doesn't exist`
`The extension is already loaded`""", colour = discord.Colour.red())
    
    try:
      
      bot.load_extension(f'cogs.{extension}')
      
      await msg.edit(embed = emb1)

    except:
      
      await msg.edit(embed = error)

@bot.command(hidden = True)
@commands.is_owner()
async def reload(ctx, extension):
    
    emb = discord.Embed(title = 'Loading...', colour = discord.Colour.blue())
    emb1 = discord.Embed(title = f'Reloaded {extension}!', colour = discord.Colour.green())
    msg = await ctx.send(embed = emb)
    await asyncio.sleep(0.5)
    error = discord.Embed(title = f"""UH! There was an error with {extension}!
>>> `The extension doesn't exist`
`The extension is not loaded yet`""", colour = discord.Colour.red())
    
    try:
      
      bot.unload_extension(f'cogs.{extension}')
      bot.load_extension(f'cogs.{extension}')
      
      await msg.edit(embed = emb1)

    except:
      
      await msg.edit(embed = error)
    

@bot.command(hidden = True)
@commands.is_owner()
async def unload(ctx, extension):
    emb = discord.Embed(title = 'Loading...', colour = discord.Colour.blue())
    emb1 = discord.Embed(title = f'Unloaded {extension}!', colour = discord.Colour.green())
    msg = await ctx.send(embed = emb)
    await asyncio.sleep(0.5)
    error = discord.Embed(title = f"""UH! There was an error with {extension}! Check this list:
>>> `The extension doesn't exist`
`The extension is already unloaded`""", colour = discord.Colour.red())
    
    try:
      
      bot.unload_extension(f'cogs.{extension}')
      
      await msg.edit(embed = emb1)

    except:
      
      await msg.edit(embed = error)

for filename in os.listdir('./cogs'):
  if filename.endswith('.py'):
    bot.load_extension(f'cogs.{filename[:-3]}')

keep_alive()
bot.run(os.environ.get("token"))