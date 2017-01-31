import unittest
from src.models.text_reader import TextReader


class TestTextReader(unittest.TestCase):
    def test_unpack_item_string(self):
        #WoW item string format is # item:itemID:enchantID:gemID1:gemID2:gemID3:gemID4:suffixID:uniqueID:linkLevel:specializationID:upgradeTypeID:instanceDifficultyID:numBonusIDs[:bonusID1:bonusID2:...][:upgradeValue1:upgradeValue2:...]:relic1NumBonusIDs[:relic1BonusID1:relic1BonusID2:...]:relic2NumBonusIDs[:relic2BonusID1:relic2BonusID2:...]:relic3NumBonusIDs[:relic3BonusID1:relic3BonusID2:...]
        #We only worry up to the bonus IDs for now.
        test_reader = TextReader()
        #Test 1: Typical input
        test_str1 = "Hitem:100:::::34:01:12:13:23:12:0:0:"
        result1 = test_reader.unpack_item_string(item_str=test_str1)
        self.assertTrue(len(result1.keys()) == 15)#All the information should be included, no extra keys for now.
        self.assertTrue(result1["item"] == "Hitem")
        self.assertTrue(result1["itemID"] == "100")
        self.assertTrue(result1["enchantID"] == "")
        self.assertTrue(result1["gemID1"] == "")
        self.assertTrue(result1["gemID2"] == "")
        self.assertTrue(result1["gemID3"] == "")
        self.assertTrue(result1["gemID4"] == "34")
        self.assertTrue(result1["suffixID"] == "01")
        self.assertTrue(result1["uniqueID"] == "12")
        self.assertTrue(result1["linkLevel"] == "13")
        self.assertTrue(result1["specializationID"] == "23")
        self.assertTrue(result1["upgradeTypeID"] == "12")
        self.assertTrue(result1["instanceDifficultyID"] == "0")
        self.assertTrue(result1["numBonusIDs"] == "0")
        self.assertTrue(len(result1["bonusIDs"]) == 0)

        #Test 2: Empty string
        test_str2 = ""
        try:
            result2 = test_reader.unpack_item_string(test_str2)
            self.assertTrue(False)
        except Exception as e:
            self.assertTrue(e.message == "Item string does not contain the minimum number of entries. 1 found when at least 14 should exist.")

        #Test 3: String that continues past bonus IDs.
        test_str3 = "Hitem:100:::::34:01:12:13:23:12:0:2:12:13::23::56:78::12"
        result3 = test_reader.unpack_item_string(item_str=test_str3)
        self.assertTrue(len(result3.keys()) == 15)  # All the information should be included, no extra keys for now.
        self.assertTrue(result3["item"] == "Hitem")
        self.assertTrue(result3["itemID"] == "100")
        self.assertTrue(result3["enchantID"] == "")
        self.assertTrue(result3["gemID1"] == "")
        self.assertTrue(result3["gemID2"] == "")
        self.assertTrue(result3["gemID3"] == "")
        self.assertTrue(result3["gemID4"] == "34")
        self.assertTrue(result3["suffixID"] == "01")
        self.assertTrue(result3["uniqueID"] == "12")
        self.assertTrue(result3["linkLevel"] == "13")
        self.assertTrue(result3["specializationID"] == "23")
        self.assertTrue(result3["upgradeTypeID"] == "12")
        self.assertTrue(result3["instanceDifficultyID"] == "0")
        self.assertTrue(result3["numBonusIDs"] == "2")
        self.assertTrue(len(result3["bonusIDs"]) == 2)

        #Test 4: String that does not continue the minimum amount of information.
        test_str4 = "Hitem:12:14:8:5"
        try:
            result4 = test_reader.unpack_item_string(item_str=test_str4)
            self.assertTrue(False)
        except Exception as e:
            self.assertTrue(e.message == "Item string does not contain the minimum number of entries. 5 found when at least 14 should exist.")

        #Test 5: Item ID is not base-10 digit string.
        test_str5 = "Hitem:0x100:::::34:01:12:13:23:12:0:0:"
        try:
            result5 = test_reader.unpack_item_string(item_str = test_str5)
            self.assertTrue(False)
        except Exception as e:
            self.assertTrue(e.message == "Item ID is not base-10 digit string. Got 0x100 instead.")
        return





if __name__ == "__main__":
    unittest.main()
