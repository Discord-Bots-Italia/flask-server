import discord
from app import keep_alive
from discord.ext import commands, tasks
import os
import json

bot = commands.Bot(command_prefix = "<")
bot.remove_command("help")
bot.load_extension("jishaku")

@bot.event
async def on_ready():
  print(f"Discord bot online as {bot.user}")
  update_count.start()
  
@bot.check
async def global_check(ctx):

  r = discord.utils.get(ctx.guild.roles, id = 613656205004636171)

  if r in ctx.author.roles:

    return True
  
  else:

    return False
  
@tasks.loop(seconds=30)
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

keep_alive()
bot.run(os.environ.get("token"))