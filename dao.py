import sqlalchemy as sy
from entities import *
from sqlalchemy.orm import sessionmaker
import os

#heroku pg:psql postgresql-animate-46261 --app msleia
class DAO:
    # engine = sy.create_engine("postgresql://mayoor@localhost/msleia")
    engine = sy.create_engine("postgres://hptuakclodksel:63dd53fb8efc1543d2b1e3b234714737c0452e76ee9bfaaafad643b2319adbb1@ec2-107-20-211-10.compute-1.amazonaws.com:5432/d3prg0hqc75pn5")

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
