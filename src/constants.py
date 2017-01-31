

class DBConst:
    engine = None
    session = None


class Codes:
    #In-game zone IDs
    instance_codes = dict()
    instance_codes["unknown"] = -1
    #Legion outdoor zones
    instance_codes["suramar"] = 7637
    instance_codes["azsuna"] = 7334
    instance_codes["highmountain"] = 7503
    instance_codes["val'sharah"] = 7558
    instance_codes["stormheim"] = 7541
    instance_codes["thunder totem"] = 7731
    instance_codes["the eye of azshara"] = 7578 #outdoor zone, instance is 'eye of azshara'

    #Legion 5-man dungeons
    instance_codes["the arcway"] = 7855
    instance_codes["vault of the wardens"] = 7787
    instance_codes["maw of souls"] = 7812
    instance_codes["return to karazhan"] = 8443
    instance_codes["black rook hold"] = 7805
    instance_codes["court of stars"] = 8079
    instance_codes["violet hold"] = 7996
    instance_codes["darkheart thicket"] = 7673
    instance_codes["eye of azshara"] = 8040
    instance_codes["neltharion's lair"] = 7546
    instance_codes["halls of valor"] = 7672

    #Legion raids
    instance_codes["trial of valor"] = 8440
    instance_codes["the nighthold"] = 8025
    instance_codes["the emerald nightmare"] = 8026

    #Emerald nightmare encounters
    en_encounters = dict()
    en_encounters["nythendra"] = 1853
    en_encounters["elerethe renferal"] = 1876
    en_encounters["il'gynoth"] = 1873
    en_encounters["ursoc"] = 1841
    en_encounters["dragons of nightmare"] = 1854
    en_encounters["cenarius"] = 1877
    en_encounters["xavius"] = 1864

    #Nighthold encounters
    nh_encounters = dict()
    nh_encounters["skorpyron"] = 1849
    nh_encounters["chronomatic anomaly"] = 1865
    nh_encounters["trilliax"] = 1867
    nh_encounters["spellblade aluriel"] = 1871
    nh_encounters["tichondrius"] = 1862
    nh_encounters["krosus"] = 1842
    nh_encounters["high botanist tel'arn"] = 1886
    nh_encounters["star augur etraeus"] = 1863
    nh_encounters["grand magistrix elisande"] = 1872
    nh_encounters["gul'dan"] = 1866


    #Difficulties
    difficulty_codes = dict()

    difficulty_codes["normal dungeon"] = 1
    difficulty_codes["heroic dungeon"] = 2
    difficulty_codes["10 player"] = 3
    difficulty_codes["25 player"] = 4
    difficulty_codes["10 player heroic"] = 5
    difficulty_codes["25 player heroic"] = 6
    difficulty_codes["looking for raid legacy"] = 7 #Pre SoO LFR
    difficulty_codes["challenge mode"] = 8
    difficulty_codes["40 player"] = 9
    difficulty_codes["heroic scneario"] = 11
    difficulty_codes["normal scenario"] = 12
    difficulty_codes["normal raid"] = 14
    difficulty_codes["heroic raid"] = 15
    difficulty_codes["mythic raid"] = 16
    difficulty_codes["looking for raid"] = 17
    difficulty_codes["event1"] = 18
    difficulty_codes["event2"] = 19
    difficulty_codes["event3"] = 20
    difficulty_codes["mythic dungeon"] = 23
    difficulty_codes["timewalker"] = 24
    difficulty_codes["pvp scenario"] = 25





