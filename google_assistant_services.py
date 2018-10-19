from tornado.web import  RequestHandler
import json
from dao import DAO 
from entities import *

dao_obj = DAO()
from commander import WebSocket
import teacher_service as teacher
from communication import StudentResponse
from communication import TeacherResponse
from communication import GAResponse

class GAActionHandler(RequestHandler):
    
    

    def post(self):
        data = json.loads(self.request.body)
        # {'responseId': '55b8db32-6f95-4b07-a7c3-54549a166976', 'queryResult': {'queryText': 'I would like to learn sight words', 'parameters': {'command': 'Sight words'}, 'allRequiredParamsPresent': True, 'fulfillmentText': 'All right! Sight words then', 'fulfillmentMessages': [{'text': {'text': ['All right! Sight words then']}}], 'outputContexts': [{'name': 'projects/leia-719a4/agent/sessions/ABwppHHaFFBRt-0kbJK_jdT0S1joKwS_6w0aQm4I_G7LnCtZyiBaRtirtg8baZMSRDv9qVJlMUcO-g/contexts/actions_capability_screen_output', 'parameters': {'command.original': 'sight words', 'command': 'Sight words'}}, {'name': 'projects/leia-719a4/agent/sessions/ABwppHHaFFBRt-0kbJK_jdT0S1joKwS_6w0aQm4I_G7LnCtZyiBaRtirtg8baZMSRDv9qVJlMUcO-g/contexts/actions_capability_audio_output', 'parameters': {'command.original': 'sight words', 'command': 'Sight words'}}, {'name': 'projects/leia-719a4/agent/sessions/ABwppHHaFFBRt-0kbJK_jdT0S1joKwS_6w0aQm4I_G7LnCtZyiBaRtirtg8baZMSRDv9qVJlMUcO-g/contexts/google_assistant_input_type_keyboard', 'parameters': {'command.original': 'sight words', 'command': 'Sight words'}}, {'name': 'projects/leia-719a4/agent/sessions/ABwppHHaFFBRt-0kbJK_jdT0S1joKwS_6w0aQm4I_G7LnCtZyiBaRtirtg8baZMSRDv9qVJlMUcO-g/contexts/actions_capability_web_browser', 'parameters': {'command.original': 'sight words', 'command': 'Sight words'}}, {'name': 'projects/leia-719a4/agent/sessions/ABwppHHaFFBRt-0kbJK_jdT0S1joKwS_6w0aQm4I_G7LnCtZyiBaRtirtg8baZMSRDv9qVJlMUcO-g/contexts/actions_capability_media_response_audio', 'parameters': {'command.original': 'sight words', 'command': 'Sight words'}}], 'intent': {'name': 'projects/leia-719a4/agent/intents/e3251622-dd3c-4957-a86d-eb73ff21e624', 'displayName': 'sw_training'}, 'intentDetectionConfidence': 1.0, 'languageCode': 'en-us'}, 'originalDetectIntentRequest': {'source': 'google', 'version': '2', 'payload': {'isInSandbox': True, 'surface': {'capabilities': [{'name': 'actions.capability.AUDIO_OUTPUT'}, {'name': 'actions.capability.WEB_BROWSER'}, {'name': 'actions.capability.MEDIA_RESPONSE_AUDIO'}, {'name': 'actions.capability.SCREEN_OUTPUT'}]}, 'requestType': 'SIMULATOR', 'inputs': [{'rawInputs': [{'query': 'I would like to learn sight words', 'inputType': 'KEYBOARD'}], 'arguments': [{'rawText': 'I would like to learn sight words', 'textValue': 'I would like to learn sight words', 'name': 'text'}], 'intent': 'actions.intent.TEXT'}], 'user': {'lastSeen': '2018-10-16T23:25:46Z', 'locale': 'en-US', 'userId': 'ABwppHFLETFcTaCxwavWZDPRsoVIGIX1aLi4135KT-bGYysWtqOU5bnmpS4AXsEqUvs8XE2RjSoWnQ'}, 'conversation': {'conversationId': 'ABwppHHaFFBRt-0kbJK_jdT0S1joKwS_6w0aQm4I_G7LnCtZyiBaRtirtg8baZMSRDv9qVJlMUcO-g', 'type': 'ACTIVE', 'conversationToken': '[]'}, 'availableSurfaces': [{'capabilities': [{'name': 'actions.capability.AUDIO_OUTPUT'}, {'name': 'actions.capability.WEB_BROWSER'}, {'name': 'actions.capability.SCREEN_OUTPUT'}]}]}}, 'session': 'projects/leia-719a4/agent/sessions/ABwppHHaFFBRt-0kbJK_jdT0S1joKwS_6w0aQm4I_G7LnCtZyiBaRtirtg8baZMSRDv9qVJlMUcO-g'}
        queryResult = data['queryResult']
        command = queryResult['parameters']['command']
        userid = data['originalDetectIntentRequest']['payload']['user']['userId']
        student_reponse = StudentResponse(userid, command)
        print (student_reponse.__dict__)
        teacher_response = teacher.get_teacher(userid).teach(student_reponse)
        WebSocket.clients[0].broadcast(WebSocket.clients,{"command":teacher_response.question})
        print (teacher_response.__dict__)
        ga_payload = GAResponse(teacher_response.prompt, teacher_response.prompt).get_json_response()
        print (ga_payload)
        self.write(ga_payload)