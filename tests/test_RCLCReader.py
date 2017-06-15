import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.constants import *
from src.db.models import *
from src.models.rclc_reader import RCLCReader
import datetime


class TestRCLCReader(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        engine = create_engine(DBConst.test_conn_str)
        Base.metadata.bind = engine
        Base.metadata.create_all()
        global DBSession
        DBSession = sessionmaker(bind=engine)
        return

    @classmethod
    def tearDownClass(cls):
        Base.metadata.drop_all()
        return

