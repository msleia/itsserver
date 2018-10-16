from flask import Flask, render_template, jsonify
from tornado.wsgi import WSGIContainer
from tornado.web import Application, FallbackHandler, RequestHandler
from tornado.ioloop import IOLoop
from tornado.websocket import WebSocketHandler
from flask_cors import CORS, cross_origin
from sockjs.tornado import SockJSRouter, SockJSConnection
import json

import tornado.web
import tornado.httpserver

import os


root = os.path.dirname(__file__)

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")

class WebSocket(SockJSConnection):
    clients = []
    def on_open(self, info):
        self.clients.append(self)
        print("Socket opened.")

    def on_message(self, message):
        self.send("Received: " + message)
        print("Received message: " + message)

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

class SendCommand(RequestHandler):
    def get(self, data):
        print ("Command received {}".format(data))
        WebSocket.clients[0].broadcast(WebSocket.clients,{"command":data})

# app = Flask(__name__)
# cors = CORS(app, resources={r"/command": {"origins": "*"}})
# # app.config['CORS_HEADERS'] = 'Access-Control-Allow-Origin'

# @app.route('/')
# def index():
#     return render_template('index.html')

if __name__ == "__main__":
    EchoRouter = SockJSRouter(WebSocket, '/command')
    # print (EchoRouter.urls)
    # container = WSGIContainer(app)
    server = Application(
        EchoRouter.urls+[(r'/sndcommand/(.*)',SendCommand), (r'/',MainHandler)], static_path=os.path.join(root,'static'), template_path=os.path.join(root,'templates'))
    port = int(os.environ.get("PORT", 8080))
    server.listen(port)
    IOLoop.instance().start()

