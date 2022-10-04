import flask
import os
from threading import Thread
import smiley_bot as bot

app = flask.Flask(__name__)

@app.route('/')
def home():
    return 'Oi, eu to vivo'

def run():
    app.run(host='0.0.0.0')

try:
    t = Thread(target=bot.run)
    t.start()
    run()
except Exception as e:
    print(e)

