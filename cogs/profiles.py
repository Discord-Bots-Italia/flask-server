import discord
from discord.ext import commands
import json

class Profiles(commands.Cog):

  def __init__(self, bot):

    self.bot = bot

  @commands.group(invoke_without_command = True)
  async def profile(self, ctx, member: discord.Member = None):

    "Guarda il profilo di un utente"

    if not member:
      
      member = ctx.author

    with open("userdata/profiles.json", "r") as f:

      l = json.load(f)

    emb = discord.Embed(colour = discord.Colour.blue(), timestamp = ctx.message.created_at)
    emb.set_thumbnail(url = member.avatar_url)

    if member.nick:

      emb.set_author(name = member.nick, icon_url = member.avatar_url)

    else:

      emb.set_author(name = member.name, icon_url = member.avatar_url)

    try:

      description = l[str(member.id)]["description"]
      projects = l[str(member.id)]["projects"]
      languages = l[str(member.id)]["languages"]

    except KeyError:
      
      description = "Nessuna descrizione"
      projects = "Nessun progetto"
      languages = "Nessun Linguaggio"

    emb.description = f"""**Descrizione**
{description}

**Progetti**
{projects}

**Linguaggi**
{languages}"""

    await ctx.send(embed = emb)

  @profile.command()
  async def create(self, ctx):

    "Crea il tuo profilo"

    with open("userdata/profiles.json", "r") as f:

      l = json.load(f)

    l[str(ctx.author.id)] = {"description": "Nessuna descrizione", "projects": "Nessun Progetto", "languages": "Nessun Linguaggio"}

    with open("userdata/profiles.json", "w") as f:

      json.dump(l, f, indent = 4)

    await ctx.send("Fatto! Ora imposta la descrizione usando `profile description <descrizione>`, i progetti con `profile projects <progetti>` e le lingue con `profile languages <lingue>`")

  @profile.command(aliases = ["descrizione"])
  async def description(self, ctx, *, description):

    "Imposta la descrizione"

    with open("userdata/profiles.json", "r") as f:

      l = json.load(f)

    try:
      
      l[str(ctx.author.id)]["description"] = str(description)
      
      with open("userdata/profiles.json", "w") as f:
        
        json.dump(l, f, indent = 4)

      await ctx.send("Fatto!")

    except KeyError:

      await ctx.send("Non hai ancora creato il tuo profilo! Usa `profile create` per crearlo.")

  

  @profile.command(aliases = ["progetti"])
  async def projects(self, ctx, *, projects):

    "Imposta i progetti"

    with open("userdata/profiles.json", "r") as f:

      l = json.load(f)

    try:
      
      l[str(ctx.author.id)]["projects"] = str(projects)
      
      with open("userdata/profiles.json", "w") as f:
        
        json.dump(l, f, indent = 4)
        
      await ctx.send("Fatto!")

    except KeyError:

      await ctx.send("Non hai ancora creato il tuo profilo! Usa `profile create` per crearlo.")

  @profile.command(aliases = ["linguaggi"])
  async def languages(self, ctx, *, languages):

    "Imposta i linguaggi"

    with open("userdata/profiles.json", "r") as f:

      l = json.load(f)

    try:
      
      l[str(ctx.author.id)]["languages"] = str(languages)

      with open("userdata/profiles.json", "w") as f:

        json.dump(l, f, indent = 4)
        
      await ctx.send("Fatto!")
    
    except KeyError:

      await ctx.send("Non hai ancora creato il tuo profilo! Usa `profile create` per crearlo.")
      
def setup(bot):
  bot.add_cog(Profiles(bot))