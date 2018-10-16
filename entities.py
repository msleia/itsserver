from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()

class SIGHT_WORDS(Base):

    __tablename__ = 'SWORDS'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    type = Column(String)
    description = Column(String)

    def __init__(self, name, code, description):
        self.name = name
        self.type = type
        self.description = description


    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
