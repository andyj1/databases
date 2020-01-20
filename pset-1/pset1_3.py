#!/bin/python3

# Sailors and Boats tables representation in SQLAlchemy ORM
# reference: lecture script
# October 2019
# Andy Jeong

from sqlalchemy import create_engine, Integer, String, Column, Boolean, DateTime, ForeignKey, PrimaryKeyConstraint, func
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
    # constraint on PK on tuple(sid, chargedate) because each sailor can be charged multiple times
    __table_args__ = (PrimaryKeyConstraint('sid', 'chargedate'), {})

    # one sailor for each payment history record
    sid = Column(Integer, ForeignKey('sailors.sid'), primary_key=True)
    # date for each payment
    chargeDate = Column(DateTime)
    # due date for each payment
    daysTillDue = Column(Integer)
    # whether paid or not
    paid = Column(Boolean)

    sailor = relationship('Sailor')

    def __init__(self, chargeDate, daysTillDue, paid, sid):
        self.sid = sid
        self.chargeDate = chargeDate
        self.daysTillDue = daysTillDue
        self.paid = paid

    def __repr__(self):
        return "<PaymentHistory(sid=%s, chargeDate='%s', daysTillDue=%s, paid=%s)>" % (self.sid, self.chargeDate, self.daysTillDue, self.paid)

class CheckupHistory(Base):
    __tablename__ = 'checkups'
    # constraint on PK on tuple(bid, lastcheckdate) because each boat can get checked multiple times
    __table_args__ = (PrimaryKeyConstraint('bid', 'lastcheckdate'), {})

    # reference to boat id
    bid = Column(Integer, ForeignKey('boats.bid'))
    # date for checkup
    lastcheckdate = Column(DateTime)
    # whether there were any problems during checkup (Integer to note level of severity)
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

# query statements
# 1. check for whether sailor id of 1 paid for all incurred charges, in descending order of chargedate
s.query(PaymentHistory.paid).filter(PaymentHistory.sid==1).order_by(PaymentHistory.chargeDate.desc())

# 2. check for how many times each boat had problem level of 2
s.query(CheckupHistory.bid, func.count()).filter(CheckupHistory.problemDetected==2)

# 3. how many boats are available now?
s.query(func.count(CurrentlyAvailable.bid)).filter(CurrentlyAvailable.available==True)