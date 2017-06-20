import urllib2
import json
from constants import Codes, DBConst

class BNet:

    def __init__(self):
        return


    def create_character_profile(self, session, name="Unknown", realm="Unknown"):
        info = self.__get_character_info(name, realm)
        return info


    def __get_character_info(self, name, realm):
        fixed_realm = realm
        url_format = u"https://us.api.battle.net/wow/character/{0}/{1}?locale=en_US&apikey={2}"
        #If we're given a realm name like 'BoreanTundra', it has to be changed to 'Borean Tundra'.
        #Unfortunately, there isn't an elegant way to do this since wow has all sorts of realm names
        #like Borean Tundra, Sen'Jin, Mug'thol, etc.
        if fixed_realm in Codes.RC_BN.keys():
            fixed_realm = Codes.RC_BN[fixed_realm]
            fixed_realm = fixed_realm.replace(" ","%20")
        url_format = url_format.format(fixed_realm, name, DBConst.BNet_Key)
        url_format = url_format.encode('utf-8')
        try:
            response = urllib2.urlopen(url_format).read()
            data = json.loads(response)
        except Exception as e:
            data = dict()
            data["player_class"] = "Unknown"
            data["player_name"] = name
            data["player_realm"] = realm
        return data