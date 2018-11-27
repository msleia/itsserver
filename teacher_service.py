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
    
class RewardManager():

    def __init__(self, userid):
        self.userid = userid
        self.reward = dao_obj.get_where(Reward,"userid = '{}' and status = 1".format(userid))
        self.has_reward = True if self.reward else False

    def get_reward_message(self):
        return self.reward.message if self.is_qualified_for_reward() else None

    def mark_exercise_complete(self):
        rstat = 1 if self.reward else 0
        erp = dao_obj.get_where(ExerciseReport,"reward_qualified = {} and rewarded = 0".format(rstat))
        erp.rewarded = 1
        dao_obj.session.commit()

    def is_qualified_for_reward(self):
        if self.reward:
            rew_ex_ct = self.reward.exercise_count if self.reward else 0
            exercise_count_qry = "select count(*) from exercise_report where user_id='{}' and reward_qualified=1 and rewarded=0 and is_completed=1"
            cursor = dao_obj.execute_query(exercise_count_qry)
            exercise_count = 0
            for rec in cursor:
                exercise_count = rec[0]

            if exercise_count == rew_ex_ct and rew_ex_ct >0 :
                return True
        return False
        
    def create_excercise_info(self, course_name):
        reward_qualified = 1 if self.has_reward else 0
        expRepo = ExerciseReport(self.userid, course_name, reward_qualified, 0, 1)
        dao_obj.put(expRepo)

class TeacherServiceHandler(RequestHandler):

    def __init__(self):
        self.userid = 0
        self.questions = []
        self.answers = []
        self.exercise = ""
        self.new_session = True
        self.current_course = None
        self.correct_answer_account = defaultdict(int)
        self.incorrect_answer_account = defaultdict(int)
        self.answer_correctness_sequence = []
        self.three_incorrect_responses = False
        self.two_incorrect_responses = False
        self.reward_manager = None

    def teach(self, student_response):
        if  self.userid == 0 or student_response.answer.lower() in ["sentences", "sentence", "sightwords", "mastered vocabulary", "sight words", "words"]:
            self.exercise = student_response.answer
            self.userid = student_response.userid
            self.reward_manager = RewardManager(self.userid)
            if self.exercise == "Sightwords":
                self.current_course = SightWordCourse('K', self.userid, max_size=5)
            elif self.exercise == "mastered vocabulary":
                self.current_course = SightWordCourse('K', self.userid, max_size=5)
            elif self.exercise.lower() == "sentences" or self.exercise.lower() == "sentence":
                self.current_course = ShortSentenceCourse('K', self.userid, max_size=5)
            else: 
                self.current_course = SightWordCourse('K', self.userid, max_size=5)

        if self.exercise == "mastered vocabulary":
            report = self.current_course.get_course_report(self.exercise)
            response = TeacherResponse(self.userid, self.exercise, report, "Here is the list.", session_complete=True)
            return response

        if not self.new_session:
            self.answers.append(student_response.answer)
        else:
            self.new_session = False

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
            self.two_incorrect_responses = (len(self.answer_correctness_sequence)>=2 and sum(self.answer_correctness_sequence[-2:])==0)

        if len(self.answers) == 0 or answer_correct or self.three_incorrect_responses:        
            question, question_id, clue = self.current_course.get_next_presentation(self.userid)
            if question:
                if answer_correct:
                    message = self.current_course.get_encouraging_feedback()+self.current_course.get_standard_query(question)
                else:
                    message = self.current_course.get_standard_query(question)
                response = TeacherResponse(self.userid, self.exercise, question, message)
                self.questions.append((question, question_id, clue))
            else:
                ## Condition where exercise is completed.
                self.reward_manager.create_excercise_info(self.exercise)
                reward_message = self.reward_manager.get_reward_message()
                if reward_message:
                    response = TeacherResponse(self.userid, self.exercise, "Exercise completed.", self.current_course.get_course_completion_phrase(), session_complete=True)
                else:
                    response = TeacherResponse(self.userid, self.exercise, "Exercise completed.", self.current_course.get_course_completion_phrase() + reward_message, session_complete=True)
        elif self.two_incorrect_responses:
            response = TeacherResponse(self.userid, self.exercise, self.questions[-1][0], self.questions[-1][2]+". "+self.current_course.get_motivating_phrase(),was_student_response_correct=False)

        else:
            response = TeacherResponse(self.userid, self.exercise, self.questions[-1][0], self.current_course.get_motivating_phrase(),was_student_response_correct=False)

        print (self.answer_correctness_sequence)
        return response

teachers = defaultdict(TeacherServiceHandler)
def get_teacher(userid):
    return teachers[userid]
