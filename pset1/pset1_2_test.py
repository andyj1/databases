from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import text

from pset1orm import Base, Sailor, Boat, Reservation
from unittest import TestCase
import unittest
import datetime

# test instance on a temporary sqlite database (so that we don't alter actual)
engineMemory = create_engine('sqlite:///:memory:')
Session = sessionmaker()
# actual database for querying
engine = create_engine('mysql+pymysql://user@localhost:3306/sailors', echo=True)

# 1. sample instances
sailor = Sailor(1000, "myname", 10, 100)
boat = Boat(1000, "myboat", "mycolor", 10)
reservation = Reservation(1000, 1000, datetime.datetime.now())

# 2. sample query
query_stmt = """SELECT avg(s.age) FROM sailors as s WHERE s.rating = 10 GROUP BY s.age"""

class TestClassInstance(TestCase):
    def setUp(self):
        # connect to the database
        self.connection = engineMemory.connect()

        # begin a non-ORM transaction
        self.trans = self.connection.begin()

        # bind an individual Session to the connection
        self.session = Session(bind=self.connection)

        Base.metadata.create_all(engineMemory)

        # add the sample instances
        self.session.add(sailor)
        self.session.add(boat)
        self.session.add(reservation)
        self.session.commit()

    def test_instance(self):
        # use the session in tests.
        # check the inserted entry against the queried result
        expected_sailor = [sailor]
        expected_boat = [boat]
        expected_reservation = [reservation]

        self.assertEqual(self.session.query(Sailor).all(), expected_sailor)
        self.assertEqual(self.session.query(Boat).all(), expected_boat)
        self.assertEqual(self.session.query(Reservation).all(), expected_reservation)

    def tearDownInstance(self):
        self.session.close()
        Base.metadata.drop_all(engineMemory)
        # rollback - everything that happened with the
        # Session above (including calls to commit())
        # is rolled back.
        self.trans.rollback()

        # return connection to the engineMemory
        self.connection.close()

class TestQuery(TestCase):
    def setUp(self):
        # connect to the database
        self.connection = engine.connect()
        # begin a non-ORM transaction
        self.trans = self.connection.begin()
        # bind an individual Session to the connection
        self.session = Session(bind=self.connection)
        Base.metadata.create_all(engine)

    def test_instance(self):
        # use the session in tests.
        # check the inserted entry against the queried result
        self.querystmt = text(query_stmt)
        result1 = self.connection.execute(self.querystmt)

        self.querystmt_orm = self.session.query(func.avg(Sailor.age)).filter(Sailor.rating==10).group_by(Sailor.age).statement.compile(compile_kwargs={"literal_binds": True})
        result2_orm = self.connection.execute(self.querystmt_orm)
        # check scalar value results
        self.assertEqual(result1.scalar(), result2_orm.scalar())

    def tearDownInstance(self):
        self.session.close()
        self.trans.rollback()
        # return connection to the engine
        self.connection.close()


if __name__== '__main__':
    unittest.main()