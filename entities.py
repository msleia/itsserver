from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DATETIME

Base = declarative_base()

class SIGHT_WORDS(Base):

    __tablename__ = 'swords'
    _table_args__ = {'quote':False,'extend_existing':True}


    id = Column(Integer, primary_key=True, autoincrement=True)
    userid = Column(String)
    name = Column(String)
    type = Column(String)
    description = Column(String)

    def __init__(self, name, type, userid, description):
        self.name = name
        self.type = type
        self.userid = userid
        self.description = description


    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class FlashCard(Base):

    __tablename__ = 'fc_master'
    _table_args__ = {'quote':False,'extend_existing':True}


    id = Column(Integer, primary_key=True, autoincrement=True)
    userid = Column(String)
    name = Column(String)
    description = Column(String)

    def __init__(self, name, userid, description):
        self.name = name
        self.userid = userid
        self.description = description

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class FlashCardSW(Base):

    __tablename__ = 'fc_words'
    _table_args__ = {'quote':False,'extend_existing':True}


    id = Column(Integer, primary_key=True, autoincrement=True)
    od = Column(Integer)
    userid = Column(String)
    flash_card_id = Column(Integer)
    sw_id = Column(Integer)

    def __init__(self, flash_card_id, userid, sw_id, order):
        self.userid = userid
        self.flash_card_id = flash_card_id
        self.sw_id = sw_id
        self.od = order

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class WordReport(Base):

    __tablename__ = 'word_report'
    _table_args__ = {'quote':False,'extend_existing':True}


    id = Column(Integer, primary_key=True, autoincrement=True)
    userid = Column(String)
    sw_id = Column(Integer)
    is_identified = Column(Integer)

    def __init__(self, userid, sw_id, is_identified):
        self.sw_id = sw_id
        self.userid = userid
        self.is_identified = is_identified


    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class UserProfile(Base):
    __tablename__ = 'user_prof'
    _table_args__ = {'quote':False,'extend_existing':True}


    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)

    def __init__(self, name):
        self.name = name


    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class FlashCardReport(Base):
    __tablename__ = 'fc_report'
    _table_args__ = {'quote':False,'extend_existing':True}


    id = Column(Integer, primary_key=True, autoincrement=True)
    userid = Column(String)
    flash_card_id = Column(Integer)
    last_accessed = Column(DATETIME)
    is_completed = Column(Integer)

    def __init__(self, userid, flash_card_id, last_accessed, is_completed):
        self.userid = userid
        self.flash_card_id = flash_card_id
        self.last_accessed = last_accessed
        self.is_completed = is_completed


    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class SentenceRepo(Base):

    __tablename__ = 'sent_repo'
    _table_args__ = {'quote':False,'extend_existing':True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    description = Column(String)

    def __init__(self, name, description):
        self.name = name
        self.description = description

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class SentenceCourseDetails(Base):

    __tablename__ = 'sent_course'
    _table_args__ = {'quote':False,'extend_existing':True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    userid = Column(String)
    sent_card_id = Column(Integer)
    sent_id = Column(Integer)

    def __init__(self, sent_card_id, sent_id, userid):
        self.sent_card_id = sent_card_id
        self.sent_id = sent_id
        self.userid = userid

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class SentenceCard(Base):
    __tablename__ = 'sent_card'
    _table_args__ = {'quote':False,'extend_existing':True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    userid = Column(String)
    name = Column(String)
    description = Column(String)
    is_completed = Column(Integer)

    def __init__(self, name, userid, description, is_completed):
        self.name = name
        self.userid = userid
        self.description = description
        self.is_completed = is_completed

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}