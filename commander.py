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
    clients = []
    user_client = {}
    def on_open(self, info):
        WebSocket.clients.append(self)
        print("Socket opened.")

    def on_message(self, message):
        print("&&Received message: " + message.strip(), type(message), message.strip())
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
        print("Socket closed.")

class SendCommand(RequestHandler):
    def get(self, data):
        print ("Command received {}".format(data))
        WebSocket.clients[0].broadcast(WebSocket.clients,{"command":data})


if __name__ == "__main__":
    EchoRouter = SockJSRouter(WebSocket, '/command')
    # print (EchoRouter.urls)
    # container = WSGIContainer(app)
    server = Application(
        EchoRouter.urls+[(r'/sndcommand/(.*)',SendCommand)])
    port = int(os.environ.get("PORT", 8080))
    server.listen(port)
    IOLoop.instance().start()

