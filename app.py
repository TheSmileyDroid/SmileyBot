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
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
except Exception as e:
    print(e)

