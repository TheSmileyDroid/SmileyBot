import flask
import os
from threading import Thread

app = flask.Flask(__name__)

@app.route('/')
def home():
    return 'Oi, eu to vivo'

@app.route('/kill')
def kill():
    os.popen('kill 1')
    return 'Server shutting down...'

def run():
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))

def keep_alive():
    server = Thread(target=run)
    server.start()
