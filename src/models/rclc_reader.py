from db.models import Player, Loot, LootAward, BonusID
from constants import DBConst, Codes
from text_reader import TextReader
from datetime import datetime
from bnet import BNet
from sqlalchemy.orm import Session
import warnings
import re

"""
Parse data and return relevant LootAward objects based on CSV format from
RC Loot Council output:
'player, date, time, item, itemID, itemString, response, votes, class, instance, boss, gear1, gear2, responseID, isAwardReason'
e.g. Thrasher-Shadowsong,07/02/17,21:45:23,[Tunic of Unwavering Devotion],140865,140865::::::::110:264::5:3:3444:1482:1813:::,BiS,6,DRUID,The Nighthold-Heroic,Trilliax,[Scarred Ragefang Chestpiece],nil,2,false

"""

def deprecated(func):
    '''This is a decorator which can be used to mark functions
    as deprecated. It will result in a warning being emitted
    when the function is used.
    Taken from https://wiki.python.org/moin/PythonDecoratorLibrary#Generating_Deprecation_Warnings'''
    def new_func(*args, **kwargs):
        warnings.warn("Call to deprecated function {}.".format(func.__name__),
                      category=DeprecationWarning)
        return func(*args, **kwargs)
    new_func.__name__ = func.__name__
    new_func.__doc__ = func.__doc__
    new_func.__dict__.update(func.__dict__)
    return new_func


class RCLCReader(TextReader):

    def __init__(self):
        TextReader.__init__(self)
        return

    #Deprecated due to changes in RCLC's CSV output no longer providing the information we need.
    @deprecated
    def read_csv_text(self, text, session):
        objects = list()
        lines = text.splitlines()
        for line in lines:
            if line == u''\
            or line == u'player, date, time, item, itemID, itemString, response,' \
                        u' votes, class, instance, boss, gear1, gear2, responseID,' \
                        u' isAwardReason':
                continue
            entry = line.split(",")
            if entry[0] == u'':
                entry.pop(0)
            player_name = entry[0].split("-")[0]
            player_realm = entry[0].split("-")[1]
            date = entry[1]
            time = entry[2]
            itemname = entry[3]
            item = entry[5]
            response = entry[6]
            votes = int(entry[7])
            wow_class = entry[8]
            instance = entry[9]
            boss = entry[10]
            gear1 = entry[11]
            gear2 = entry[12]
            responseID = entry[13]
            is_award_reason = entry[14]
            instance_id = instance.split("-")[0]
            instance_id = Codes.instance_codes[instance_id.lower()]
            existing_player = session.query(Player)\
                            .filter(Player.name == player_name, Player.realm == player_realm).all()
            player = None
            if(len(existing_player) == 1):
                player = existing_player[0]
            elif(len(existing_player) > 1):
                raise Exception("Multiple existing player_rel "
                                "with name {0} and realm {1} found in DB.".format(player_name, player_realm))
            else:
                player = Player(name = player_name, realm = player_realm)
                session.add(player)
            iteminfo = self.unpack_item_string("Hitem:"+item.split("|")[2])
            #RCLC output does not match the actual Wow item string format in that it removes the starting 'hitem'.
            existing_loot = session.query(Loot)\
                            .filter(Loot.item_id == int(iteminfo["itemID"])).all()
            new_time = datetime.strptime(date, "%d/%m/%y")
            new_loot = LootAward(reason = response, player_rel = player, award_date = new_time)
            session.add(new_loot)
            if len(existing_loot) == 1:
                new_loot.item_rel = existing_loot[0]
            elif len(existing_loot) > 1:
                raise Exception("Multiple loot instances of item {0} found.".format(existing_loot[0].item_id))
            else:
                _loot = Loot(item_id = int(iteminfo["itemID"]), instance = instance_id, name=itemname)
                session.add(_loot)
                new_loot.item_rel = _loot
            if gear1 != "nil":
                gear1info = self.unpack_item_string("Hitem:"+gear1.split("|")[2])
                gear1name = gear1.split("|")[3]
                gear1name = gear1name[2:-1]
                existing_gear1 = session.query(Loot).filter(Loot.item_id == int(gear1info["itemID"])).all()
                if len(existing_gear1) == 1:
                    new_loot.replacement1_rel = existing_gear1[0]
                elif len(existing_gear1) > 1:
                    raise Exception("Multiple loot instances of item {0} found.".format(existing_gear1[0].item_id))
                else:
                    _replacement1 = Loot(item_id=int(gear1info["itemID"]), instance=-1, name=gear1name)
                    session.add(_replacement1)
                    new_loot.replacement1_rel = _replacement1
            else:
                new_loot.replacement1_rel = None
            if gear2 != "nil":
                gear2info = self.unpack_item_string("Hitem"+gear2.split("|")[2])
                gear2name = gear2.split("|")[3]
                gear2name = gear2name[2:-1]
                existing_gear2 = session.query(Loot) \
                    .filter(Loot.item_id == int(gear2info["itemID"])).all()
                if len(existing_gear2) == 1:
                    new_loot.replacement2_rel = existing_gear2[0]
                elif len(existing_gear2) > 1:
                    raise Exception("Multiple loot instances of item {0} found.".format(existing_gear2[0].item_id))
                else:
                    _replacement2 = Loot(item_id=int(gear2info["itemID"]), instance=-1, name=gear2name)
                    session.add(_replacement2)
                    new_loot.replacement2_rel = _replacement2
            else:
                new_loot.replacement2_rel = None
            objects.append(new_loot)
        return objects

    def read_tsv_text(self, text, session):
        """

        :param text: Lines of TSV text representing loot council data. Lines should match
        player	date	time	item	itemID	itemString	response	votes	class	instance	boss	gear1	gear2	responseID	isAwardReason
        format.
        :param session: Database session new loot awards should be added to.
        :return: The LootAward objects created and added to the session.
        """
        objects = list()
        lines = text.splitlines()
        for line in lines:
            if line == u''\
                or line == u'player	date	time	item	itemID	itemString	response' \
                           u'	votes	class	instance	boss	gear1	gear2' \
                           u'	responseID	isAwardReason':
                continue
            data = line.split("\t")
            player_name = data[0].split("-")[0]
            player_realm = data[0].split("-")[1]
            date = datetime.strptime(data[1], "%d/%m/%y")
            time = data[2]
            itemHL = data[3]
            itemID = int(data[4])
            itemString = data[5]
            response = data[6]
            votes = data[7]
            wow_class = data[8]
            instance = data[9]
            boss = data[10]
            gear1HL = data[11]
            gear2HL = data[12]
            responseID = data[13]
            isAwardReason = data[14]

            item_name = itemHL.split(",")[1]
            item_name = item_name[1:-2]

            gearIDregex = "wowhead.com/item=([0-9]+)"
            gearBonusRegex = "&bonus=([0-9-:]+)"
            gear1_name = gear1HL.split("\",")[1]
            gear1_name = gear1_name[1:-2]
            if gear1_name != u"nil":
                gear1IDgroups = re.search(gearIDregex, gear1HL)
                gear1ID = int(gear1IDgroups.group(1))
                gear1BonusGroups = re.search(gearBonusRegex, gear1HL)
                if gear1BonusGroups is not None:
                    gear1_bonus_IDs = gear1BonusGroups.group(1).split(":")
                    gear1_bonus_IDs = [int(i) for i in gear1_bonus_IDs]
                else:
                    gear1_bonus_IDs = list()

            gear2_name = gear2HL.split("\",")[1]
            gear2_name = gear2_name[1:-2]
            if gear2_name != u"nil":
                gear2IDgroups = re.search(gearIDregex, gear2HL)
                gear2ID = int(gear2IDgroups.group(1))
                gear2BonusGroups = re.search(gearBonusRegex, gear2HL)
                if gear2BonusGroups is not None:
                    gear2_bonus_IDs = gear2BonusGroups.group(1).split(":")
                    gear2_bonus_IDs = [int(i) for i in gear2_bonus_IDs]
                else:
                    gear2_bonus_IDs = list()

            instance_id = Codes.instance_codes[instance.split("-")[0].lower()]
            player = None
            existing_player = session.query(Player)\
                .filter(Player.name == player_name, Player.realm == player_realm).all()
            if len(existing_player) == 1:
                player = existing_player[0]
            elif len(existing_player) > 1:
                raise Exception("Multiple existing players with name {0} and realm {1} found."
                                .format(player_name, player_realm))
            else:
                bnet = BNet()
                player_info = bnet.create_character_profile(session, name=player_name, realm=player_realm)
                player = Player(name=player_name, realm=player_realm, wow_class=player_info["class"])
                session.add(player)
            item_info = self.unpack_item_string("Hitem:"+itemString)
            #RCLC output does not match the actual WoW item string format, it removes the starting "hitem",
            #we add it here to preserve the purity of unpack_item_string

            new_award = LootAward(reason=response, player_rel=player, award_date=date)
            session.add(new_award)

            existing_items = session.query(Loot).filter(Loot.item_id == itemID).all()
            item_info["bonusIDs"] = [int(i) for i in item_info["bonusIDs"]]
            matching = list()
            for item in existing_items:
                all_matching = True
                if len(item.bonus_ids) != len(item_info["bonusIDs"]):
                    all_matching = False
                for id in item.bonus_ids:
                    if id.bonus_id not in item_info["bonusIDs"]:
                        all_matching = False
                        break
                if all_matching:
                    matching.append(item)
            if len(matching) == 1:
                new_award.item_rel = matching[0]
            elif len(matching) > 1:
                raise Exception("Multiple loot instances of item {0} with bonus IDs {1} found."
                                .format(matching[0].item_id, item_info["bonusIDs"]))
            else:
                new_item = Loot(item_id = itemID, instance = instance_id, name=item_name)
                session.add(new_item)
                new_award.item_rel = new_item
                for id in item_info["bonusIDs"]:
                    new_item.bonus_ids.append(BonusID(bonus_id=id))

            #We just get wowhead hyperlinks instead of item strings for the gear replacement, so itemID
            #and bonus IDs extraction is different than how we do it with the awarded item.

            if gear1_name != u"nil":
                existing_gear1 = session.query(Loot).filter(Loot.item_id == gear1ID).all()
                matching = list()
                for item in existing_gear1:
                    all_matching = True
                    if len(item.bonus_ids) != len(gear1_bonus_IDs):
                        all_matching = False
                    for id in item.bonus_ids:
                        if id.bonus_id not in gear1_bonus_IDs:
                            all_matching = False
                            break
                    if all_matching:
                        matching.append(item)
                if len(matching) == 1:
                    new_award.replacement1_rel = matching[0]
                elif len(matching) > 1:
                    raise Exception("Multiple loot instances of item {0} with bonus IDs {1} found."
                                    .format(matching[0].item_id, gear1_bonus_IDs))
                else:
                    new_gear1 = Loot(item_id = gear1ID, instance = -1, name=gear1_name)
                    session.add(new_gear1)
                    new_award.replacement1_rel = new_gear1
                    for id in gear1_bonus_IDs:
                        new_gear1.bonus_ids.append(BonusID(bonus_id=id))

            if gear2_name != u"nil":
                existing_gear2 = session.query(Loot).filter(Loot.item_id == gear2ID).all()
                matching = list()
                for item in existing_gear2:
                    all_matching = True
                    if len(item.bonus_ids) != len(gear2_bonus_IDs):
                        all_matching = False
                    for id in item.bonus_ids:
                        if id.bonus_id not in gear2_bonus_IDs:
                            all_matching = False
                            break
                    if all_matching:
                        matching.append(item)
                if len(matching) == 1:
                    new_award.replacement2_rel = matching[0]
                elif len(matching) > 1:
                    raise Exception("Multiple loot instances of item {0} with bonus IDs {1} found."
                                    .format(matching[0].item_id, gear2_bonus_IDs))
                else:
                    new_gear2 = Loot(item_id = gear2ID, instance = -1, name=gear2_name)
                    session.add(new_gear2)
                    new_award.replacement2_rel = new_gear2
                    for id in gear2_bonus_IDs:
                        new_gear2.bonus_ids.append(BonusID(bonus_id=id))
            objects.append(new_award)
        return objects



