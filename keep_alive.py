from flask import Flask 
from threading import Thread 
 
app = Flask('')
 
@app.route('/')
def home():
    return("You found this bot? Now what? https://discord.com/api/oauth2/authorize?client_id=945584374756306985&permissions=8&scope=bot%20applications.commands is the invite link!")
 
def run():
  app.run(host='0.0.0.0',port=8080)
 
def keep_alive():
    t = Thread(target=run)
    t.start()