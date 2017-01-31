


class TextReader():

    def __init__(self):
        return

    def unpack_item_string(self,item_str):
        # We need to parse out the item now. It's so dumb.
        # As of 7.0.3, this is the format:
        # item:itemID:enchantID:gemID1:gemID2:gemID3:gemID4:suffixID:uniqueID:linkLevel:specializationID:upgradeTypeID:instanceDifficultyID:numBonusIDs[:bonusID1:bonusID2:...][:upgradeValue1:upgradeValue2:...]:relic1NumBonusIDs[:relic1BonusID1:relic1BonusID2:...]:relic2NumBonusIDs[:relic2BonusID1:relic2BonusID2:...]:relic3NumBonusIDs[:relic3BonusID1:relic3BonusID2:...]
        # The item CSV output from RC is something like
        # |cffa335ee|Hitem:139219::::::::110:264::6:4:1806:42:1507:3336:::|h[Black Venom Sabatons]|h|r
        # So have fun matching it up.
        iteminfo = dict()
        splititem = item_str.split(":")
        iteminfo["item"] = splititem[0]
        iteminfo["itemID"] = splititem[1]
        iteminfo["enchantID"] = splititem[2]
        iteminfo["gemID1"] = splititem[3]
        iteminfo["gemID2"] = splititem[4]
        iteminfo["gemID3"] = splititem[5]
        iteminfo["gemID4"] = splititem[6]
        iteminfo["suffixID"] = splititem[7]
        iteminfo["uniqueID"] = splititem[8]
        iteminfo["linkLeveL"] = splititem[9]
        iteminfo["specializationID"] = splititem[10]
        iteminfo["upgradeTypeID"] = splititem[11]
        iteminfo["instanceDifficultyID"] = splititem[12]
        iteminfo["numBonusIDs"] = splititem[13]
        iteminfo["bonusIDs"] = list()
        index = 14
        for i in range(0, int(iteminfo["numBonusIDs"])):
            iteminfo["bonusIDs"].append(splititem[index])
            index += 1
        return iteminfo