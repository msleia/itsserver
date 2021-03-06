class TeacherResponse():
    def __init__(self, userid, exercise_type, question, prompt, session_complete=False, was_student_response_correct=True):
        self.userid = userid
        self.exercise_type = exercise_type
        self.question = question
        self.prompt = prompt
        self.session_complete = session_complete
        self.was_student_response_correct = was_student_response_correct

class TeacherQuery():
    def __init__(self, userid, prompt):
        pass

class StudentResponse():
    def __init__(self, userid, answer):
        self.userid = userid
        self.answer = answer

class StudentQuery():
    pass

class GAResponse():
    def __init__(self,speech, displayText):
        self.speech = speech
        self.displayText = displayText

    def get_json_response(self, expect_response=True):
        # res = {
        #     "speech": self.speech,  
        #     "displayText": self.displayText,
        #     "data": {
        #         "google": {
        #         "expect_user_response": True,
        #         "is_ssml": False,
        #         "permissions_request": {
        #             "opt_context": "",
        #             "permissions": [
                    
        #             ]
        #         }
        #         }
        #     },
        #     "contextOut": [],
        # }
        # res = {
        #     "speech": self.speech,  
        #     "displayText": self.displayText,
        #     "data": {
        #         "google": {
        #         "expect_user_response": True,
        #         "is_ssml": False
        #         }
        #     },
        #     "contextOut": [],
        # }

        res = {
            "payload": {
                "google": {
                "expectUserResponse": expect_response,
                "richResponse": {
                    "items": [
                    {
                        "simpleResponse": {
                            "textToSpeech": self.speech
                        }
                    }
                    ]
                }
                }
            }
        }
        return res


