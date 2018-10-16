from tornado.web import  RequestHandler
import json
from dao import DAO 
from entities import *

dao_obj = DAO()

class GAActionHandler(RequestHandler):
    def post(self):
        data = json.loads(self.request.body)
        print (data)
    
