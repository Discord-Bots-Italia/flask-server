from flask import Flask, render_template, redirect, g, session, request, url_for, jsonify
from threading import Thread
import json
import os
from requests_oauthlib import OAuth2Session
from wtforms import Form, StringField, TextAreaField, validators
import requests

OAUTH2_CLIENT_ID = os.environ['OAUTH2_CLIENT_ID']
OAUTH2_CLIENT_SECRET = os.environ['OAUTH2_CLIENT_SECRET']
OAUTH2_REDIRECT_URI = 'http://www.discordbotsitalia.tk/callback'

API_BASE_URL = os.environ.get('API_BASE_URL', 'https://discordapp.com/api')
AUTHORIZATION_BASE_URL = API_BASE_URL + '/oauth2/authorize'
TOKEN_URL = API_BASE_URL + '/oauth2/token'
app = Flask(__name__)
app.config['SECRET_KEY'] = OAUTH2_CLIENT_SECRET
class BotForm(Form):
  nome = StringField("Nome",[validators.Length(min=1,max=32)])
  botid = StringField("Bot id",[validators.Length(min=18,max=18)])
  invito = StringField("Invito",[validators.Length(min=1,max=200)])
if 'http://' in OAUTH2_REDIRECT_URI:
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = 'true'

def token_updater(token):
    session['oauth2_token'] = token

def make_session(token=None, state=None, scope=None):
    return OAuth2Session(
        client_id=OAUTH2_CLIENT_ID,
        token=token,
        state=state,
        scope=scope,
        redirect_uri=OAUTH2_REDIRECT_URI,
        auto_refresh_kwargs={
            'client_id': OAUTH2_CLIENT_ID,
            'client_secret': OAUTH2_CLIENT_SECRET,
        },
        auto_refresh_url=TOKEN_URL,
        token_updater=token_updater)
        
@app.route('/login')
def login():
    scope = request.args.get(
        'scope',
        'identify guilds')
    discord = make_session(scope=scope.split(' '))
    authorization_url, state = discord.authorization_url(AUTHORIZATION_BASE_URL)
    session['oauth2_state'] = state
    return redirect(authorization_url)
    
@app.route('/callback')
def callback():

    if request.values.get('error'):
        return request.values['error']
    print(session.get("oauth2_state"))
    discord = make_session(state = session.get('oauth2_state'))

    token = discord.fetch_token(
        TOKEN_URL,
        client_secret = OAUTH2_CLIENT_SECRET,
        authorization_response=request.url)
    session['oauth2_token'] = token
    
    return redirect("https://www.discordbotsitalia.tk/me")

@app.route('/me')
def me():
  
    discord = make_session(token=session.get('oauth2_token'))
    user = discord.get(API_BASE_URL + '/users/@me').json()
    guilds = discord.get(API_BASE_URL + '/users/@me/guilds').json()
    
    if user["id"] == "446650423416193034":
      return "sei bello"
    else:
      return f"{user['username']}, sei come miky"

@app.route('/')
def home():
  return render_template("index.html")

@app.route("/bot")
def bot():
  return render_template("bot.html")

@app.route("/mobile")
def mobile():
  return render_template("mobile/index.html")

@app.route("/mobile/bot")
def mobile_bot():
  return render_template("mobile/bot.html")

@app.route("/index")
def fake_index():
  return redirect("/")

@app.route("/index.html")
def fake_index_html():
  return redirect("/")

@app.route("/stats") 
def _membri():#ah salve?
  
  with open("shit.json") as f:
    stats = json.load(f)
    
  return render_template("stats.html",online=stats["online"],dnd=stats["dnd"],idle=stats["idle"],offline=stats["offline"],bots=stats["bots"])#{{membri}}

@app.route("/join")
def join():
  return render_template("join_embed.html")

@app.route("/mobile/join")
def mobile_join():
  return render_template("join_embed.html")

@app.route("/mobile/stats") 
def mobile_membri():
  
  with open("shit.json") as f:
    stats = json.load(f)
    
  return render_template("mobile/stats.html",online=stats["online"],dnd=stats["dnd"],idle=stats["idle"],offline=stats["offline"],bots=stats["bots"])

@app.route("/addbot")
def test_me():

  return render_template("addbot.html")

@app.route("/allbots")
def all_bots():

  l = requests.get("https://dbiapi.ssebastianoo.repl.co/api").json()
    
  res = ""

  for a in l:

    res += f"<a class = 'logo' href = 'https://discordapp.com/api/oauth2/authorize?client_id={l[str(a)]['id']}&permissions=0&scope=bot' target = '_blank'><img src = '{l[str(a)]['avatar_url']}' alt = '{a}' width = '100px'></a>\n<div class = 'text'><a class = 'botname'><em>{a} ({l[str(a)]['status']})</em></a></div>\n<br>\n"

  html0 = '''<!DOCTYPE html>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width">
  <title>Lista Bot</title>
  <link href="https://fonts.googleapis.com/css?family=Roboto+Mono&display=swap" rel="stylesheet">
  <link rel="icon" href="https://cdn.discordapp.com/icons/611322575674671107/a_97c421382d72ed131956e0deb51aa1f7.gif?size=1024"/>
  <meta property = "og:title" content = "Discord Bots Italia">
  <meta property = "og:description" content = "Tutti i bot listati nel server">
  <meta property = "og:image" content = "https://cdn.discordapp.com/icons/611322575674671107/a_97c421382d72ed131956e0deb51aa1f7.gif?size=1024">
  <meta name="theme-color" content="#706fd3">
  
  <style>
      body {
        background: #706fd3;
        margin-top: 50px;
        font-family: 'Roboto Mono', monospace;
        margin-right: 10%;
        margin-left: 35%;
      }
      
      h1 {
        color: #273c75;
      }

      .nolink {
        text-decoration: none;
      }

      .link {
        color: #182C61;
      }
  
      .container {
        margin-left: 20%;
        margin-right: 20%;
      }

      .logo {
        float: left;
        padding: 12.5px;
      }

      div {
        padding: 50px;
      }

      a {
        font-size: 20px;
      }

      img {
        transition-duration: .3s;
      }

      img:hover {
        width: 110px;
      }

  </style>
    
</head>
<body>'''

  html1 = f'''\n  {res}'''

  html2 = """\n<script>
    if (/Android|webOS|iPhone|iPad|iPod|BlackBerry|BB|PlayBook|IEMobile|Windows Phone|Kindle|Silk|Opera Mini/i.test(navigator.userAgent)) {
      location.href = 'mobile/allbots';
    }

  </script>
    
</body>
  """

  with open("templates/all-bots.html", "w") as f:

    f.write(" ")
    f.write(html0)
    f.write(html1)
    f.write(html2)
  
  return render_template("all-bots.html")

@app.route("/mobile/allbots")
def mobile_all_bots():

  l = requests.get("https://dbiapi.ssebastianoo.repl.co/api").json()
    
  res = ""

  for a in l:

    res += f"<a class = 'logo' href = 'https://discordapp.com/api/oauth2/authorize?client_id={l[str(a)]['id']}&permissions=0&scope=bot' target = '_blank'><img src = '{l[str(a)]['avatar_url']}' alt = '{a}' width = '100px'></a>\n<div class = 'text'><a class = 'botname'><em>{a} ({l[str(a)]['status']})</em></a></div>\n<br>\n"

  html0 = '''<!DOCTYPE html>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width">
  <title>Lista Bot</title>
  <link href="https://fonts.googleapis.com/css?family=Roboto+Mono&display=swap" rel="stylesheet">
  <link rel="icon" href="https://cdn.discordapp.com/icons/611322575674671107/a_97c421382d72ed131956e0deb51aa1f7.gif?size=1024"/>
  <meta property = "og:title" content = "Discord Bots Italia">
  <meta property = "og:description" content = "Tutti i bot listati nel server">
  <meta property = "og:image" content = "https://cdn.discordapp.com/icons/611322575674671107/a_97c421382d72ed131956e0deb51aa1f7.gif?size=1024">
  <meta name="theme-color" content="#706fd3">
  
  <style>
      body {
        background: #706fd3;
        margin-top: 50px;
        font-family: 'Roboto Mono', monospace;
      }
      
      h1 {
        color: #273c75;
      }

      .nolink {
        text-decoration: none;
      }

      .link {
        color: #182C61;
      }
  
      .container {
        margin-left: 20%;
        margin-right: 20%;
      }

      .logo {
        float: left;
        padding: 14px;
      }

      div {
        padding: 50px;
      }

      a {
        font-size: 20px;
      }

      img {
        transition-duration: .3s;
      }

      img:hover {
        width: 110px;
      }

  </style>
    
</head>
<body>'''

  html1 = f'\n  {res}\n</body>'

  with open("templates/mobile/all-bots.html", "w") as f:

    f.write(" ")
    f.write(html0)
    f.write(html1)

  return render_template("mobile/all-bots.html")

@app.route("/api/bots")
def api_bots():

  return redirect("https://dbiapi.ssebastianoo.repl.co/api")

@app.errorhandler(404)
def not_found(error):  return render_template("404.html")

@app.errorhandler(500)
def internal_error(error):
  return render_template("500.html", error = error)

def keep_alive():  
    t = Thread(target=run)
    t.start()

def run():
  app.run(host='0.0.0.0',port=8080)