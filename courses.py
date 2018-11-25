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

    @abc.abstractmethod
    def get_course_report(self, report_type):
        pass

    def get_motivating_phrase(self):
        return random.choice(["Can you try that again?", "Try again."])

    def get_encouraging_feedback(self):
        return random.choice(["Good job!", "Let us try another one.", "Good. Let us keep going.", "Awesome!", "You are so good at it!"])

    def get_course_completion_phrase(self):
        return "Congratulations! You just completed a reading exercise. Let us practice this again tomorrow. Good bye!"

class ShortSentenceCourse(Course):
    def __init__(self, level, userid, max_size=6):
        self.curr_word = None
        self.curr_word_index = 0
        self.level = level
        self.userid = userid
        self.max_size = max_size
        self.sentence_course_id = None
        self.sentences = self.generate_sentence_course(userid)

    def get_mastered_words(self):
        query_word_report = 'select sum(is_identified) as mastery, sw_id, sw.name, type, wr.userid from word_report wr, swords sw where wr.sw_id=sw.id and wr.userid=\'{}\' group by wr.userid, sw_id, sw.name, type having sum(is_identified) > 0 order by mastery desc'.format(self.userid)
        cursor = dao_obj.execute_query(query_word_report)
        word_mastery_list = []
        for rec in cursor:
            word_mastery_list.append({'user':rec[4], 'type':rec[3], 'word':rec[2], 'word_id':rec[1], 'identified_count':rec[0]})
        return word_mastery_list

    def generate_sentence_course(self, userid):

        sent_card = dao_obj.get_where(SentenceCard, "userid = '{}' and is_completed = {}".format(userid, 0))
        self.sentence_course_id = sent_card
        selected_sentences = []
        if not sent_card:
            sc = SentenceCard("sc_{}_{}".format(self.userid, self.level),self.userid, "{} sentence card for {}".format(self.level, self.userid), 0)
            sc = dao_obj.put(sc)
            self.sentence_course_id = sc

            word_list = self.get_mastered_words()
            words = [mw['word'].lower() for mw in word_list]
            sent_list = dao_obj.get_all(SentenceRepo)
            course_sentences = []
            print ("*****************************************************************************************")
            print (words)
            print ("*****************************************************************************************")
            for sent in sent_list:
                print ("-----------------------------------------------------------------------------------------------")
                good = True
                for w in sent.name.lower().split(' '):
                    print (w, sent.name)
                    if w not in words:
                        good = False
                        break
                if good:
                    course_sentences.append(SentenceCourseDetails(sc.id,sent.id,self.userid))
                    selected_sentences.append((sent.name, sent.id))
                if len(selected_sentences) >= self.max_size:
                    break
                print ("-----------------------------------------------------------------------------------------------")
            for scd in course_sentences:
                dao_obj.put(scd)

        else:
            sentence_list_query = "select sr.name, sr.id from sent_repo sr, sent_course sc where sc.sent_id=sr.id and sent_card_id={}".format(sent_card.id)
            cursor = dao_obj.execute_query(sentence_list_query)
            for rec in cursor:
                selected_sentences.append((rec[0], rec[1]))
            print ("$$$$$$$$$$$", selected_sentences)

        return selected_sentences

    def get_standard_query(self, question=None):
        return "Can you try reading this sentence?"
    
    def get_next_presentation(self, curr_presentation):
        if self.curr_word_index == len(self.sentences):
            self.curr_word = ''
            self.sentence_course_id.is_completed = 1
            dao_obj.session.commit()
            return (None,None)
        else:
            self.curr_word = self.sentences[self.curr_word_index]
            self.curr_word_index += 1
        # print (len(self.flashcard), self.curr_word_index, self.curr_word, "Why is this empty")
        return self.curr_word


    def verify_response(self, response, question):
        res_correctness = True
        res_words = response.lower().split()
        print (question)
        for qw in question[0].split(' '):
            if qw not in res_words:
                res_correctness = False
        print (res_correctness, question, response.split(' '))
        # wr = WordReport(self.userid, question[1], 1 if res_correctness else 0)
        # dao_obj.put(wr)
        return res_correctness

    def get_course_report(self, report_type):
        pass

class SightWordCourse(Course):

    def __init__(self, level, userid, max_size=10):
        self.curr_word = None
        self.curr_word_index = 0
        self.level = level
        self.userid = userid
        self.max_size = max_size
        self.flash_card_id = None
        self.flashcard = self.generate_flashcard(userid)

    def get_standard_query(self, question=None):
        if self.curr_word_index == 1 and question:
            return "This word is pronounced {}. Can you repeat that?".format(question)
        return "What is the word that you see?"

    def get_mastered_words(self):
        query_word_report = 'select sum(is_identified) as mastery, sw_id, sw.name, type, wr.userid from word_report wr, swords sw where wr.sw_id=sw.id and wr.userid=\'{}\' group by wr.userid, sw_id, sw.name, type having sum(is_identified) > 0 order by mastery desc'.format(self.userid)
        cursor = dao_obj.execute_query(query_word_report)
        word_mastery_list = []
        for rec in cursor:
            word_mastery_list.append({'user':rec[4], 'type':rec[3], 'word':rec[2], 'word_id':rec[1], 'identified_count':rec[0]})
        return word_mastery_list

    def get_next_presentation(self, curr_presentation):
        if self.curr_word_index == len(self.flashcard):
            self.curr_word = ''
            self.flash_card_id.is_completed = 1
            dao_obj.session.commit()
            return (None,None)
        else:
            self.curr_word = self.flashcard[self.curr_word_index]
            self.curr_word_index += 1
        # print (len(self.flashcard), self.curr_word_index, self.curr_word, "Why is this empty")
        return self.curr_word

    def generate_flashcard(self, userid):
        flash_card = dao_obj.get_where(FlashCardReport, "userid = '{}' and is_completed = {}".format(userid, 0))
        self.flash_card_id = flash_card
        # FlashCardSW
        selected_words = []

        if not flash_card:
            fc_word_list = []
            known_words = []
            mwords = self.get_mastered_words()
            all_mastered_words = [w['word'] for w in mwords]
            words = dao_obj.get_all(SIGHT_WORDS)
            if len(mwords) > self.max_size-1:
                kwords_indexes = random.sample(range(0,len(mwords)),self.max_size-1)

                known_words = [(w['word'], w['word_id']) for w in [mwords[ik] for ik in kwords_indexes]]
            
                for word in words:
                    if word.name not in all_mastered_words:
                        fc_word_list = [(word.name, word.id)] + known_words
                        break
                if len(fc_word_list) < self.max_size:
                    fc_word_list = [(mwords[-1]['word'], mwords[-1]['word_id'])] + known_words
            else:
                windexes = random.sample(range(0,len(words)),len(mwords)-self.max_size)
                fc_word_list += [(words[index].name, words[index].id) for index in windexes]
            fc = FlashCard("fc_{}_{}".format(self.userid, self.level),self.userid, "{} flash card for {}".format(self.level, self.userid))
            fc = dao_obj.put(fc)
            self.flash_card_id = fc
            fc_obj_list = []
            print (fc_word_list, len(mwords), len(words))
            for index in range(len(fc_word_list)):
                # selected_words.append((words[index].name, words[index].id))
                fc_obj_list.append(FlashCardSW(fc.id,self.userid,fc_word_list[index][1], index))
            for fcw in fc_obj_list:
                fcw.flash_card_id = fc.id
                dao_obj.put(fcw)
            fc_report = FlashCardReport(self.userid, fc.id, None, 0)
            dao_obj.put(fc_report)
            selected_words = fc_word_list
            print ("*******", selected_words)
        else:
            word_list_query = "SELECT sw.name, sw.id FROM fc_words FCW, swords sw WHERE FCW.flash_card_id={} and FCW.sw_id=sw.id order by FCW.od asc".format(flash_card.flash_card_id)
            cursor = dao_obj.execute_query(word_list_query)
            for rec in cursor:
                selected_words.append((rec[0], rec[1]))
            print ("$$$$$$$$$$$", selected_words)
        ir_word_list = [selected_words[0],selected_words[1]]
        wind = 1
        for i in range(2,len(selected_words)):
            ir_word_list.append(selected_words[0])
            for k in range(i):
                ir_word_list.append(selected_words[wind+k])
        print ('~~~~~~~~~~~~~', ir_word_list)
        return ir_word_list

    def get_course_report(self, report_type):
        return {"mastered_vocab":self.get_mastered_words()}


    def verify_response(self, response, question):
        res_correctness = True if question[0] in response.split(' ') else False
        print (res_correctness, question, response.split(' '))
        wr = WordReport(self.userid, question[1], 1 if res_correctness else 0)
        dao_obj.put(wr)
        return res_correctness
