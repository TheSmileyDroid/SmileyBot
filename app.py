import flask
import os
from threading import Thread
import smiley_bot as bot

app = flask.Flask(__name__)

@app.route('/')
def home():
    return 'Oi, eu to vivo'


try:
    t = Thread(target=bot.run)
    t.start()
except Exception as e:
    print(e)

