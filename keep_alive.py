import flask
import os
from threading import Thread

app = flask.Flask('')

@app.route('/')
def home():
  return 'Oi, eu to vivo'

def run():
  app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))

def keep_alive():
  t = Thread(target=run)
  t.start()
