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
        self.correct_answer_account = defaultdict(int)
        self.incorrect_answer_account = defaultdict(int)
        self.answer_correctness_sequence = []
        self.three_incorrect_responses = False

    def teach(self, student_response):
        if  self.userid == 0:
            self.exercise = student_response.answer
            self.userid = student_response.userid
            if self.exercise == "Sightwords":
                self.current_course = SightWordCourse('K', self.userid, max_size=5)
            else: 
                self.current_course = SightWordCourse('K', self.userid, max_size=5)
        else:
            self.answers.append(student_response.answer)

        answer_correct = False
        if len(self.answers) > 0:
            answer_correct = self.current_course.verify_response(self.answers[-1], self.questions[-1])
            if answer_correct:
                self.correct_answer_account[self.questions[-1][0]] += 1
                self.answer_correctness_sequence.append(1)
            else:
                self.incorrect_answer_account[self.questions[-1][0]] += 1
                self.answer_correctness_sequence.append(0)                

            self.three_incorrect_responses = (len(self.answer_correctness_sequence)>=3 and sum(self.answer_correctness_sequence[-3:])==0)

        if len(self.answers) == 0 or answer_correct or self.three_incorrect_responses:        
            question, question_id = self.current_course.get_next_presentation(self.userid)
            if question:
                response = TeacherResponse(self.userid, self.exercise, question, self.current_course.get_standard_query(question))
                self.questions.append((question, question_id))
            else:
                response = TeacherResponse(self.userid, self.exercise, "Exercise completed.", self.current_course.get_course_completion_phrase(), session_complete=True)
        else:
            response = TeacherResponse(self.userid, self.exercise, self.questions[-1][0], self.current_course.get_motivating_phrase())

        print (self.answer_correctness_sequence)
        return response

teachers = defaultdict(TeacherServiceHandler)
def get_teacher(userid):
    return teachers[userid]
