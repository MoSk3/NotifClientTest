from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, logger=True, engineio_logger=True, debug=True)
socketio.init_app(app, cors_allowed_origins="*")

iot_devices = []
clients = []

class Client:
    @staticmethod
    def get_client(sid):
        for c in clients:
            if c.sid == sid:
                return c
        return None

    def __init__(self, sid):
        self.sid = sid
        self.connected = True
        clients.append(self)


    # Emits data to a socket's unique room
    def emit(self, event, data):
        emit(event, data, room=self.sid, namespace="/")

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.post('/send_notif')
def send_notif():
    for c in iot_devices:
        c.emit('notif', None)
    return 'Ok'

@socketio.on('message')
def handle_message(msg):
    if msg == 'subscribe_notif':
        client = Client.get_client(request.sid)
        print(client)
        if client is not None:
            iot_devices.append(client)
            
    print('received message: ' + msg)


@socketio.on('connect')
def test_connect():
    try:
        sid = request.sid
        client = Client(sid)
        print('Connected ' + client.sid)
    except:
        pass



@socketio.on('disconnect')
def test_disconnect():
    try:
        sid = request.sid
        client = Client.get_client(sid)
        if client is not None:
            iot_devices.remove(client);
            print('Disconnected ' + client.sid)
    except:
        pass


if __name__ == '__main__':
    socketio.run(app)
    app.run(host="192.168.0.126", Debug=True)