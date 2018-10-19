class TeacherResponse():
    def __init__(self, userid, exercise_type, question, prompt):
        self.userid = userid
        self.exercise_type = exercise_type
        self.question = question
        self.prompt = prompt

class TeacherQuery():
    def __init__(self, userid, prompt):
        pass

class StudentResponse():
    def __init__(self, userid, answer):
        self.userid = userid
        self.answer = answer

class StudentQuery():
    pass