from tornado.wsgi import WSGIContainer
from tornado.web import Application, FallbackHandler, RequestHandler
from tornado.ioloop import IOLoop
from tornado.websocket import WebSocketHandler
from sockjs.tornado import SockJSRouter, SockJSConnection
import json

import tornado.web
import tornado.httpserver

import os


class WebSocket(SockJSConnection):
    # clients = []
    user_client = {}
    def __init__(self, **kwargs):
        super.__init__(**kwargs)
        self.sock_key = ''
    def on_open(self, info):
        # WebSocket.clients.append(self)
        print("Socket opened.")

    def on_message(self, message):
        print("&&Received message: " + message.strip(), type(message), message.strip())
        vals = message.split('\n')
        if vals[0] == 'SEND' and len(vals) > 1:
            ms_payload = eval(vals[1][12:]) if vals[1].startswith('destination:') else {}
            if 'message' in ms_payload:
                print ("Exctracted message is ", ms_payload)
                print ('user name is: ', ms_payload['message']['username'].strip())
                WebSocket.user_client[ms_payload['message']['username'].strip()] = self
                self.sock_key = ms_payload['message']['username'].strip()
            else:
                print ('no idea what i received')
        self.send(json.dumps({"received":message}))

    def send_message(self, message, data_type):
        """
        Standard format for all messages
        """
        return self.send(json.dumps({
            'data_type': data_type,
            'data': message,
        }))

    def on_close(self):
        WebSocket.user_client.pop(self.sock_key, None)
        print("Socket closed.")

class SendCommand(RequestHandler):
    def get(self, data):
        print ("Command received {}".format(data))
        sockets = [WebSocket.user_client[k] for k in WebSocket.user_client]
        sockets[0].broadcast(sockets,{"command":data})


if __name__ == "__main__":
    EchoRouter = SockJSRouter(WebSocket, '/command')
    # print (EchoRouter.urls)
    # container = WSGIContainer(app)
    server = Application(
        EchoRouter.urls+[(r'/sndcommand/(.*)',SendCommand)])
    port = int(os.environ.get("PORT", 8080))
    server.listen(port)
    IOLoop.instance().start()

