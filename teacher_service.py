from tornado.web import  RequestHandler

from dao import DAO 
from entities import *
from collections import defaultdict
from courses import *
dao_obj = DAO()
from communication import TeacherResponse

class TeachSightWordServiceHandler(RequestHandler):

    def show_word(self, currword):
        pass
    
class TeachFCGenHandler(RequestHandler):
    def generate_flash_card(self, userid):
        pass
    
class TeacherServiceHandler(RequestHandler):

    def __init__(self):
        self.userid = 0
        self.questions = []
        self.answers = []
        self.exercise = ""
        self.current_course = None

    def teach(self, student_response):
        if  self.userid == 0:
            self.exercise = student_response.answer
            self.userid = student_response.userid
            if self.exercise == "Sightwords":
                self.current_course = SightWordCourse('K', self.userid)
            else: 
                self.current_course = SightWordCourse('K', self.userid)
                
        question = self.current_course.get_next_presentation(self.userid)
        response = TeacherResponse(self.userid, self.exercise, question, self.current_course.get_standard_query())
        return response

teachers = defaultdict(TeacherServiceHandler)
def get_teacher(userid):
    return teachers[userid]
