
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
    payload structure = {"words":[{"word":"he", "type":"K", "description":"Dolch", "clues":""}], "userid":123}
    """
    def post(self):
        sw = tornado.escape.json_decode(self.request.body)
        words = sw["words"]
        for word in words:
            dao_obj.put(SIGHT_WORDS(word['word'],word['type'],sw['userid'],word['description'], word['clues']))


    
class SentenceHandler(RequestHandler):
    def get(self):
        actions = dao_obj.get_all(SentenceRepo)
        data = {'sentences':[act.to_dict() for act in actions]}
        self.write(data)

    """
    payload structure = {"sentences":[{"sentence":"thank you", "description":"Dolch"}]}
    """
    def post(self):
        sw = tornado.escape.json_decode(self.request.body)
        sents = sw["sentences"]
        for sent in sents:
            dao_obj.put(SentenceRepo(sent['sentence'],sent['description']))


class RewardHandler(RequestHandler):
    def get(self):
        actions = dao_obj.get_where(Reward,"status = 1")
        data = {'sentences':[act.to_dict() for act in actions]}
        self.write(data)

    """
    payload structure = {"reward":{"message":"Mommy is so proud of you. She has a surprise for you! Go and Collect it.", "exercise_count":1, "userid":"123@gmail.com"}}
    """
    def post(self):
        sw = tornado.escape.json_decode(self.request.body)
        reward = sw["reward"]
        # userid, message, exercise_count, status
        rw_active = dao_obj.get_where(Reward,"userid = '{}' and status = 1".format(reward['userid']))
        if rw_active:
            rw_active.status = 0
            dao_obj.session.commit()
        dao_obj.put(Reward(reward['userid'],reward['message'],reward['exercise_count'], 1))


class EncMsgHandler(RequestHandler):
    def get(self):
        actions = dao_obj.get_all(EncMessages)
        data = {'messages':[act.to_dict() for act in actions]}
        self.write(data)

    """
    payload structure = {"messages":[{"message":"You are doing awesome"}]}
    """
    def post(self):
        sw = tornado.escape.json_decode(self.request.body)
        msgs = sw["messages"]
        for msg in msgs:
            dao_obj.put(EncMessages(msg['message']))

