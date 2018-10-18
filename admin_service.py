
from tornado.web import  RequestHandler
import tornado
from dao import DAO 
from entities import *

dao_obj = DAO()

class SightWordHandler(RequestHandler):
    def get(self):
        actions = dao_obj.get_all(SIGHT_WORDS)
        data = {'sightwords':[act.to_dict() for act in actions]}
        self.write(data)

    """
    payload structure = {"words":[{"word":"he", "type":"K", "description","Dolch"}], "userid":123}
    """
    def post(self):
        sw = tornado.escape.json_decode(self.request.body)
        words = sw["words"]
        for word in words:
            dao_obj.put(SIGHT_WORDS(word['word'],word['type'],sw['userid'],word['description']))


    
 