from tornado.wsgi import WSGIContainer
from tornado.web import Application, FallbackHandler, RequestHandler
from tornado.ioloop import IOLoop
from tornado.websocket import WebSocketHandler
from sockjs.tornado import SockJSRouter, SockJSConnection
from admin_service import SightWordHandler

import json

import tornado.web
import tornado.httpserver

import os

from commander import WebSocket
from commander import SendCommand

root = os.path.dirname(__file__)

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")

def main():
    EchoRouter = SockJSRouter(WebSocket, '/command')
    server = Application(
        EchoRouter.urls+[(r'/sndcommand/(.*)',SendCommand), 
        (r'/',MainHandler),
        (r'/sightwords/all', SightWordHandler)
        ], static_path=os.path.join(root,'static'), template_path=os.path.join(root,'templates')

    )
    port = int(os.environ.get("PORT", 8080))
    server.listen(port)
    IOLoop.instance().start()


if __name__ == "__main__":
    main()