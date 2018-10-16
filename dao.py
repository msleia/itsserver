import sqlalchemy as sy
from entities import *
from sqlalchemy.orm import sessionmaker

class DAO:
    engine = sy.create_engine("postgresql://mayoor@localhost/msleia")
    sessionmaker = sessionmaker(bind=engine)
    session = sessionmaker()

    def get_all(self, cls):
        return DAO.session.query(cls).all()

    def get_where(self, cls, condition):
        return DAO.session.query(cls).filter(sy.text(condition)).first()

    def get_item(self, cls, id):
        return DAO.session.query(cls).filter_by(id=id).first()

    def put(self, object):
        DAO.session.add(object)
        DAO.session.commit()
