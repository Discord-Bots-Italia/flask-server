from flask import Flask, render_template
from threading import Thread
import json
app = Flask(__name__)

@app.route('/')
def hello():
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

@app.route("/stats")
def _membri():#ah salve?
  
  with open("shit.json") as f:
    stats = json.load(f)
    
  return render_template("stats.html",online=stats["online"],dnd=stats["dnd"],idle=stats["idle"],offline=stats["offline"],bots=stats["bots"])#{{membri}}
  
@app.errorhandler(404)
def not_found(e):
  return render_template("404.html")

def keep_alive():  
    t = Thread(target=run)
    t.start()

def run():
  app.run(host='0.0.0.0',port=8080)



