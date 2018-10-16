
from tornado.web import  RequestHandler

from dao import DAO 
from entities import *

dao_obj = DAO()

class SightWordHandler(RequestHandler):
    def get(self):
        actions = dao_obj.get_all(SIGHT_WORDS)
        data = {'sightwords':[act.to_dict() for act in actions]}
        return data
    
 