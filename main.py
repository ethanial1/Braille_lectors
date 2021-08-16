from flask import Flask, render_template
from flask_socketio import SocketIO, send

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('message')
def handleMessage(msg):
    print("Mensaje: ",msg)
    send(msg, broadcast = True)

socketio.run(app, host='0.0.0.0', port=443 )  