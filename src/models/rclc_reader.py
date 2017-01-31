from db.models import Player, Loot, LootAward
from constants import DBConst, Codes
from text_reader import TextReader
from datetime import datetime
import re

"""
Parse data and return relevant LootAward objects based on CSV format from
RC Loot Council output:
'player, date, time, item, itemID, response, votes, class, instance, boss, gear1, gear2, responseID, isAwardReason'
e.g. ,Akiroar-BoreanTundra,01/01/17,21:12:55,|cffa335ee|Hitem:139219::::::::110:264::6:4:1806:42:1507:3336:::|h[Black Venom Sabatons]|h|r,139219,Need,3,HUNTER,The Emerald Nightmare-Mythic,Elerethe Renferal,|cffa335ee|Hitem:142422::::::::110:253::5:2:3468:1492:::|h[Radiant Soul Sabatons]|h|r,nil,2,false,
"""
class RCLCReader(TextReader):

    def __init__(self):
        TextReader.__init__(self)
        return

    def read_csv_text(self, text):
        objects = list()
        lines = text.splitlines()
        session = DBConst.session
        #session.begin_nested()
        for line in lines:
            if line == u'player, date, time, item, itemID, response, votes, class, instance, boss,' \
                       u' gear1, gear2, responseID, isAwardReason':
                continue
            entry = line.split(",")
            if entry[0] == u'':
                entry.pop(0)
            player_name = entry[0].split("-")[0]
            player_realm = entry[0].split("-")[1]
            date = entry[1]
            time = entry[2]
            item = entry[3]
            response = entry[5]
            votes = int(entry[6])
            wow_class = entry[7]
            instance = entry[8]
            boss = entry[9]
            gear1 = entry[10]
            gear2 = entry[11]
            responseID = entry[12]
            is_award_reason = entry[13]
            instance_id = instance.split("-")[0]
            instance_id = Codes.instance_codes[instance_id.lower()]
            existing_player = session.query(Player)\
                            .filter(Player.name == player_name, Player.realm == player_realm).all()
            player = None
            if(len(existing_player) == 1):
                player = existing_player[0]
            elif(len(existing_player) > 1):
                session.rollback()
                raise Exception("Multiple existing players "
                                "with name {0} and realm {1} found in DB.".format(player_name, player_realm))
            else:
                player = Player(name = player_name, realm = player_realm)
                session.add(player)
            iteminfo = self.unpack_item_string(item.split("|")[2])
            existing_loot = session.query(Loot)\
                            .filter(Loot.item_id == int(iteminfo["itemID"])).all()
            new_loot = LootAward(reason = response, player = player, date = datetime.strptime(date, "%d/%m/%y"))
            session.add(new_loot)
            if len(existing_loot) == 1:
                new_loot.item = existing_loot[0]
            elif len(existing_loot) > 1:
                session.rollback()
                raise Exception("Multiple loot instances of item {0} found.".format(existing_loot[0].item_id))
            else:
                _loot = Loot(item_id = int(iteminfo["itemID"]), instance = instance_id)
                session.add(_loot)
                new_loot.item = _loot
            if gear1 != "nil":
                gear1info = self.unpack_item_string(gear1.split("|")[2])
                existing_gear1 = session.query(Loot).filter(Loot.item_id == int(gear1info["itemID"])).all()
                if len(existing_gear1) == 1:
                    new_loot.replacement1 = existing_gear1[0]
                elif len(existing_gear1) > 1:
                    session.rollback()
                    raise Exception("Multiple loot instances of item {0} found.".format(existing_gear1[0].item_id))
                else:
                    _replacement1 = Loot(item_id=int(gear1info["itemID"]), instance=-1)
                    session.add(_replacement1)
                    new_loot.replacement1 = _replacement1
            else:
                new_loot.replacement1 = None
            if gear2 != "nil":
                gear2info = self.unpack_item_string(gear2.split("|")[2])
                existing_gear2 = session.query(Loot) \
                    .filter(Loot.item_id == int(gear2info["itemID"])).all()
                if len(existing_gear2) == 1:
                    new_loot.replacement1 = existing_gear2[0]
                elif len(existing_gear2) > 1:
                    session.rollback()
                    raise Exception("Multiple loot instances of item {0} found.".format(existing_gear2[0].item_id))
                else:
                    _replacement2 = Loot(item_id=int(gear2info["itemID"]), instance=-1)
                    session.add(_replacement2)
                    new_loot.replacement1 = _replacement2
            else:
                new_loot.replacement2 = None
            objects.append(new_loot)
        return objects


