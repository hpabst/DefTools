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

    def test_read_csv_text(self):
        reader = RCLCReader()
        session = DBSession()
        #Test case 1: typical input.
        test_str1 = """player, date, time, item, itemID, response, votes, class, instance, boss, gear1, gear2, responseID, isAwardReason
,Berrimond-Shadowsong,05/01/17,20:59:55,|cffa335ee|Hitem:138216::::::::110:264::6:2:1806:1502:::|h[Horror Inscribed Chestguard]|h|r,138216,Mainspec Bis,6,PALADIN,The Emerald Nightmare-Mythic,Ysondre,|cffa335ee|Hitem:139224::::::::110:70::6:3:1806:43:1502:::|h[Insect-Etched Chestplate]|h|r,nil,1,false,
,Merimack-Shadowsong,05/01/17,20:59:50,|cffa335ee|Hitem:139205::::::::110:264::6:3:1806:1512:3336:::|h[Cowl of Fright]|h|r,139205,Need,4,MONK,The Emerald Nightmare-Mythic,Ysondre,|cffa335ee|Hitem:139205::::::::110:270::3:2:1807:1472:::|h[Cowl of Fright]|h|r,nil,2,false,"""
        result1 = reader.read_csv_text(test_str1, session)
        session.commit()
        self.assertTrue(len(result1) == 2)
        self.assertTrue(result1[0].player_rel.name == "Berrimond")
        self.assertTrue(result1[0].player_rel.realm == "Shadowsong")
        self.assertTrue(result1[0].reason == "Mainspec Bis")
        self.assertTrue(result1[0].award_date == datetime.date(year=2017, month=01, day=05))
        self.assertTrue(result1[0].item_rel.item_id == 138216)
        self.assertTrue(result1[0].item_rel.instance == Codes.instance_codes["the emerald nightmare"])
        self.assertTrue(result1[0].replacement1_rel.item_id == 139224)
        self.assertTrue(result1[0].replacement2_rel == None)

        self.assertTrue(result1[1].player_rel.name == "Merimack")
        self.assertTrue(result1[1].player_rel.realm == "Shadowsong")
        self.assertTrue(result1[1].reason == "Need")
        self.assertTrue(result1[1].award_date == datetime.date(year=2017, month=01, day=05))
        self.assertTrue(result1[1].item_rel.item_id == 139205)
        self.assertTrue(result1[1].item_rel.instance == Codes.instance_codes["the emerald nightmare"])
        self.assertTrue(result1[1].replacement1_rel.item_id == 139205)
        self.assertTrue(result1[1].replacement2_rel == None)

        return
