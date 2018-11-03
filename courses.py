import abc
from entities import *
from dao import DAO
import random
dao_obj = DAO()
import time

class Course:
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def get_next_presentation(self,curr_presentation):
        pass
    
    @abc.abstractmethod
    def get_standard_query(self):
        pass

    @abc.abstractmethod
    def verify_response(self, response, question):
        pass

    def get_motivating_phrase(self):
        return random.choice(["Can you try that again?", "Try again"])

class SightWordCourse(Course):

    def __init__(self, level, userid):
        self.curr_word = None
        self.curr_word_index = 0
        self.level = level
        self.userid = userid
        self.flashcard = self.generate_flashcard(userid)

    def get_standard_query(self):
        return "What is the word that you see?"
        
    def get_next_presentation(self, curr_presentation):
        if self.curr_word_index+1 == len(self.flashcard):
            self.curr_word_index == 0
        else:
            self.curr_word_index += 1
        return self.flashcard[self.curr_word_index]

    def generate_flashcard(self, userid):
        flash_card = dao_obj.get_where(FlashCardReport, "userid = '{}' and is_completed = {}".format(userid, 0))
        # FlashCardSW
        selected_words = []

        if not flash_card:
            fc_word_list = []
            words = dao_obj.get_all(SIGHT_WORDS)
            windexes = random.sample(range(0,len(words)),20)
            fc = FlashCard("fc_{}_{}".format(self.userid, self.level),self.userid, "{} flash card for {}".format(self.level, self.userid))
            fc = dao_obj.put(fc)
            for index in windexes:
                selected_words.append((words[index].name, words[index].id))
                fc_word_list.append(FlashCardSW(fc.id,self.userid,words[index].id))
            for fcw in fc_word_list:
                fcw.flash_card_id = fc.id
                dao_obj.put(fcw)
            fc_report = FlashCardReport(self.userid, fc.id, None, 0)
            dao_obj.put(fc_report)

        else:
            word_list_query = "SELECT sw.name, sw.id FROM fc_words FCW, swords sw WHERE FCW.flash_card_id={} and FCW.sw_id=sw.id".format(flash_card.flash_card_id)
            cursor = dao_obj.execute_query(word_list_query)
            for rec in cursor:
                selected_words.append((rec[0], rec[1]))
        return selected_words

    def verify_response(self, response, question):
        res_correctness = True if question[0] in response.split(' ') else False
        print (res_correctness, question, response.split(' '))
        wr = WordReport(self.userid, question[1], 1 if res_correctness else 0)
        dao_obj.put(wr)
        return res_correctness
