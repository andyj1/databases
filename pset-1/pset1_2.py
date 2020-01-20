#!/bin/python3

# Sailors and Boats tables representation in SQLAlchemy ORM
# reference: lecture script, https://docs.sqlalchemy.org/en/13/orm/basic_relationships.html
# October 2019
# Andy Jeong

from sqlalchemy import create_engine, Integer, String, Column, DateTime, ForeignKey, PrimaryKeyConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, backref, relationship

# user: has all privileges, host at 'localhost', port: 3306 (default), database: 'sailors'
engine = create_engine('mysql+pymysql://user@localhost:3306/sailors', echo=True)
conn = engine.connect()
Base = declarative_base()
session = sessionmaker(bind=engine)
s = session()

class Sailor(Base):
    __tablename__ = 'sailors'

    sid = Column(Integer, primary_key=True)
    sname = Column(String)
    rating = Column(Integer)
    age = Column(Integer)

    # one-to-many relationship b/w sailor-boat
    # boats = relationship('Boat', backref='Boat')
    
    def __init__(self, sid, sname, rating, age):
        self.sid = sid
        self.sname = sname
        self.rating = rating
        self.age = age

    def __repr__(self):
        return "<Sailor(id=%s, name='%s', rating=%s, age=%s)>" % (self.sid, self.sname, self.rating, self.age)


class Boat(Base):
    __tablename__ = 'boats'

    bid = Column(Integer, primary_key=True)
    bname = Column(String)
    color = Column(String)
    length = Column(Integer)


    # one-to-many relationship b/w boat-reservation, with cascade delete
    reservations = relationship('Reservation',
                                backref=backref('boat', cascade='delete'))
    # sailors = relationship('Sailor', foreign_keys='Sailor.sid', back_populates="boats")
    # boat_sid = Column(Integer, ForeignKey('Sailor.sid'))
    
    def __init__(self, bid, bname, color, length):
        self.bid = bid
        self.bname = bname
        self.color = color
        self.length = length

    def __repr__(self):
        return "<Boat(id=%s, name='%s', color=%s)>" % (self.bid, self.bname, self.color)

class Reservation(Base):
    __tablename__ = 'reserves'
    __table_args__ = (PrimaryKeyConstraint('sid', 'bid', 'day'), {})

    sid = Column(Integer, ForeignKey('sailors.sid'))
    bid = Column(Integer, ForeignKey('boats.bid'))
    day = Column(DateTime)

    sailor = relationship('Sailor') # one-to-many relationship b/w sailor-reservation

    def __init__(self, sid, bid, day):
        self.sid = sid
        self.bid = bid
        self.day = day

    def __repr__(self):
        return "<Reservation(sid=%s, bid=%s, day=%s)>" % (self.sid, self.bid, self.day)

# qr = s.query(Sailor, Boat, Reservation)
# for row in qr:
#     print(row)
