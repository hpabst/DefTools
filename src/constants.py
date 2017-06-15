

class DBConst:
    conn_str = 'sqlite:///deftools.db'
    test_conn_str = 'sqlite:///../src/db/deftools_test.db'
    BNet_Key = "pcdpw9tpsyj4cqr6z8mg7ehpwpgwevaq"

class ClassColours:
    dk_rgb = (196, 31, 59)
    dh_rgb = (163, 48, 201)
    druid_rgb = (255, 125, 10)
    hunter_rgb = (171, 212, 115)
    mage_rgb = (105, 204, 240)
    monk_rgb = (0, 255, 150)
    paladin_rgb = (245, 140, 186)
    priest_rgb = (255, 255, 255)
    rogue_rgb = (255, 245, 105)
    shaman_rgb = (0, 112, 222)
    warlock_rgb = (148, 130, 201)
    warrior_rgb = (199, 156, 110)

    dk_hex = "#C41F3B"
    dh_hex = "#A330C9"
    druid_hex = "#FF7D0A"
    hunter_hex = "#ABD473"
    mage_hex = "#69CCF0"
    monk_hex = "#00FF96"
    paladin_hex = "#F58CBA"
    priest_hex = "#FFFFFF"
    rogue_hex = "#FFF569"
    shaman_hex = "#0070DE"
    warlock_hex = "#9482C9"
    warrior_hex = "#C79C6E"




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

    #Class Codes
    class_codes = dict()
    class_codes["WARRIOR"] = 1
    class_codes["PALADIN"] = 2
    class_codes["HUNTER"] = 3
    class_codes["ROGUE"] = 4
    class_codes["PRIEST"] = 5
    class_codes["DEATHKNIGHT"] = 6
    class_codes["SHAMAN"] = 7
    class_codes["MAGE"] = 8
    class_codes["WARLOCK"] = 9
    class_codes["MONK"] = 10
    class_codes["DRUID"] = 11
    class_codes["DEMONHUNTER"] = 12

    #Realm names, mapping from the output provided by RCLootCouncil to WoW API names
    RC_BN = dict()

    RC_BN["Aegwynn"] = "Aegwynn"
    RC_BN["AeriePeak"] = "Aerie Peak"
    RC_BN["Agmaggan"] = "Agmaggan"
    RC_BN["Aggramar"] = "Aggramar"
    RC_BN["Akama"] = "Akama"
    RC_BN["Alexstrasza"] = "Alexstrasza"
    RC_BN["Alleria"] = "Alleria"
    RC_BN["AltarofStorms"] = "Alter of Storms"
    RC_BN["AlteracMountains"] = "Alterac Mountains"
    RC_BN["Aman'Thul"] = "Aman'Thul"
    RC_BN["Andorhal"] = "Andorhal"
    RC_BN["Anetheron"] = "Anetheron"
    RC_BN["Antonidas"] = "Antonidas"
    RC_BN["Anub'arak"] = "Anub'arak"
    RC_BN["Anvilmar"] = "Anvilmar"
    RC_BN["Arathor"] = "Arathor"
    RC_BN["Archimonde"] = "Archimonde"
    RC_BN["Area52"] = "Area 52"
    RC_BN["ArgentDawn"] = "Argent Dawn"
    RC_BN["Arthas"] = "Arthas"
    RC_BN["Arygos"] = "Arygos"
    RC_BN["Auchindoun"] = "Auchindoun"
    RC_BN["Azgalor"] = "Azgalor"
    RC_BN["Azjol-Nerub"] = "Azjol-Nerub"
    RC_BN["Azralon"] = "Azralon"
    RC_BN["Azshara"] = "Azshara"
    RC_BN["Azuremyst"] = "Azuremyst"
    RC_BN["Baelgun"] = "Baelgun"
    RC_BN["Balnazzar"] = "Balnazzar"
    RC_BN["Barthilas"] = "Barthilas"
    RC_BN["BlackDragonflight"] = "Black Dragonflight"
    RC_BN["Blackhand"] = "Blackhand"
    RC_BN["Blackrock"] = "Blackrock"
    RC_BN["BlackwaterRaiders"] = "Blackwater Raiders"
    RC_BN["BlackwingLair"] = "Blackwing Lair"
    RC_BN["Blade'sEdge"] = "Blade's Edge"
    RC_BN["Bladefist"] = "Bladefist"
    RC_BN["BleedingHollow"] = "Bleeding Hollow"
    RC_BN["BloodFurnace"] = "Blood Furnace"
    RC_BN["Bloodhoof"] = "Bloodhoof"
    RC_BN["Bloodscalp"] = "Bloodscalp"
    RC_BN["Bonechewer"] = "Bonechewer"
    RC_BN["BoreanTundra"] = "Borean Tundra"





