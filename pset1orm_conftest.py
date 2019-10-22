from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from pset1orm import Base, Sailor, Boat, Reservation
from unittest import TestCase
import unittest
import datetime

Session = sessionmaker()
engine = create_engine('sqlite:///:memory:')
# sample instances
sailor = Sailor(1000, "myname", 10, 100)
boat = Boat(1000, "myboat", "mycolor", 10)
reservation = Reservation(1000, 1000, datetime.datetime.now())

class TestQuery(TestCase):
    def setUp(self):
        # connect to the database
        self.connection = engine.connect()

        # begin a non-ORM transaction
        self.trans = self.connection.begin()

        # bind an individual Session to the connection
        self.session = Session(bind=self.connection)

        Base.metadata.create_all(engine)

        # add the sample instances
        self.session.add(sailor)
        self.session.add(boat)
        self.session.add(reservation)
        self.session.commit()

    def test_query(self):
        # use the session in tests.
        # check the inserted entry against the queried result
        expected_sailor = [sailor]
        expected_boat = [boat]
        expected_reservation = [reservation]

        self.assertEqual(self.session.query(Sailor).all(), expected_sailor)
        self.assertEqual(self.session.query(Boat).all(), expected_boat)
        self.assertEqual(self.session.query(Reservation).all(), expected_reservation)

    def tearDown(self):
        self.session.close()
        Base.metadata.drop_all(engine)
        # rollback - everything that happened with the
        # Session above (including calls to commit())
        # is rolled back.
        self.trans.rollback()

        # return connection to the Engine
        self.connection.close()

if __name__== '__main__':
    unittest.main()