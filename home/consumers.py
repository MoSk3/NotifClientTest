import json
from channels.generic.websocket import WebsocketConsumer

# class Client:
#     @staticmethod
#     def get_client(sid):
#         for c in clients:
#             if c.sid == sid:
#                 return c
#         return None

#     def __init__(self, sid):
#         self.sid = sid
#         self.connected = True
#         clients.append(self)


#     # Emits data to a socket's unique room
#     def emit(self, event, data):
#         emit(event, data, room=self.sid, namespace="/")

class IoTDeviceConsumer(WebsocketConsumer):
    @staticmethod
    def send_notif_all():
        for c in iot_devices:
            c.send('notif')
    
    def connect(self):
        self.accept()
        iot_devices.append(self)

    def disconnect(self, close_code):
        iot_devices.remove(self)

    def receive(self, text_data):
        print(text_data)
        IoTUserConsumer.send_sensor_data(text_data)

class IoTUserConsumer(WebsocketConsumer):
    @staticmethod
    def send_sensor_data(val):
        for c in iot_users:
            c.send(val)

    def connect(self):
        self.accept()
        iot_users.append(self)

    def disconnect(self, close_code):
        iot_users.remove(self)

    def receive(self, text_data):
        print(text_data)
        IoTDeviceConsumer.send_notif_all()


iot_devices: list[IoTDeviceConsumer] = []
iot_users: list[IoTUserConsumer] = []
