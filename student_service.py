from tornado.web import  RequestHandler

from dao import DAO 
from entities import *

dao_obj = DAO()

class StudentServiceHandler(RequestHandler):

    def get(self, st_exs_id, currword):
        return {"cat":"cat"}
        
 