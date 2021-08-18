from src.clasificador import clasificadorBraille
from src.imagen import Imagen
from src.procesamiento import Procesamiento
from flask import Flask, render_template
from flask_socketio import SocketIO, send

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('message')
def handleMessage(msg):
    # creamos los objetos
    clasificador = clasificadorBraille()
    img =  Imagen(msg)
    procs = Procesamiento(image = img)

    for letra in procs:
        clasificador.push(letra)
    
    result = clasificador.obtener_resultado()     
    send(result)

if __name__ == '__main__':
    socketio.run(app, logger=True, engineio_logger=True)  