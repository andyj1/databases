#!/bin/python3

# Sailors and Boats tables representation in SQLAlchemy ORM
# reference: lecture script
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

class PaymentHistory(Base):
    __tablename__ = 'payments'
    __table_args__ = (PrimaryKeyConstraint('sid', 'chargeate'), {})

    sid = Column(Integer, ForeignKey('sailors.sid'), primary_key=True)
    chargeDate = Column(DateTime)
    daysTillDue = Column(Integer)
    paid = Column(Boolean)

    sailor = relationship('Sailor')

    def __init__(self, chargeDate, daysTillDue, paid):
        self.sid = sid
        self.chargeDate = chargeDate
        self.daysTillDue = daysTillDue
        self.paid = paid

    def __repr__(self):
        return "<PaymentHistory(sid=%s, chargeDate='%s', daysTillDue=%s, paid=%s)>" % (self.sid, self.chargeDate, self.daysTillDue, self.paid)

class CheckupHistory(Base):
    __tablename__ = 'checkups'
    __table_args__ = (PrimaryKeyConstraint('bid', 'lastcheckdate'), {})

    bid = Column(Integer, ForeignKey('boats.bid'))
    lastcheckdate = Column(DateTime)
    problemDetected = Column(Integer)

    boat = relationship('Boat')

    def __init__(self, bid, lastcheckdate, problemDetected):
        self.bid = bid
        self.lastcheckdate = lastcheckdate
        self.problemDetected = problemDetected

    def __repr__(self):
        return "<checkupHistory(bid=%s, lastcheckdate=%s, problemDetected=%s)>)" % (self.bid, self.lastcheckdate, self.problemDetected)

class CurrentlyAvailable(Base):
    __tablename__ = 'availableBoats'

    bid = Column(Integer, ForeignKey('boats.bid'), primary_true=True)
    available = Column(Boolean)

    boat = relationship('Boat')

    def __init__(self, bid, available):
        self.bid = bid
        self.available = available

    def __repr__(self):
        return "<currentlyAvailable(bid=%s, available=%s)>" % (self.bid, self.available)


