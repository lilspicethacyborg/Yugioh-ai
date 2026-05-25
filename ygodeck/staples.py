"""Curated knowledge base of generic staple cards by category."""

HANDTRAPS = [
    ("Ash Blossom & Joyous Spring", 3, "Universal hand trap"),
    ("Maxx \"C\"", 3, "Draw-based punish for Special Summons"),
    ("Effect Veiler", 3, "Monster effect negation"),
    ("Infinite Impermanence", 3, "Monster negation, also negates column"),
    ("Nibiru, the Primal Being", 3, "Punishes 5+ summons"),
    ("Ghost Ogre & Snow Rabbit", 3, "Destroys activated effects"),
    ("Droll & Lock Bird", 3, "Shuts down searching"),
    ("Ghost Belle & Haunted Mansion", 3, "Negates GY interaction"),
    ("D.D. Crow", 3, "Banishes from GY"),
    ("Artifact Lancea", 3, "Prevents banishing"),
    ("PSY-Framegear Gamma", 3, "Negates when you control no monsters"),
    ("Dimension Shifter", 3, "Banishes everything for a turn"),
    ("Ghost Mourner & Moonlit Chill", 3, "Punishes Special Summoned monsters"),
    ("Skull Meister", 3, "Negates GY effects"),
    ("Token Collector", 3, "Destroys tokens"),
    ("Mulcharmy Fuwalos", 3, "Draw on Special Summons from Deck"),
    ("Mulcharmy Purulia", 3, "Draw on add-to-hand effects"),
    ("Mulcharmy Nyalus", 3, "Draw on send-to-GY effects"),
    ("Contact \"C\"", 3, "Punishes Extra Deck summons"),
]

BOARD_BREAKERS = [
    ("Lightning Storm", 3, "Destroys all ATK or Spell/Trap"),
    ("Harpie's Feather Duster", 1, "Destroys all opponent Spell/Traps"),
    ("Raigeki", 1, "Destroys all opponent monsters"),
    ("Dark Hole", 3, "Destroys all monsters"),
    ("Forbidden Droplet", 3, "Negates and halves ATK"),
    ("Super Polymerization", 3, "Uses opponent's monsters as Fusion material"),
    ("Evenly Matched", 3, "Forces banish all but 1"),
    ("Lava Golem", 3, "Tributes 2 opponent monsters"),
    ("Triple Tactics Talent", 3, "Draw 2 / steal / peek"),
    ("Book of Moon", 3, "Flips monster face-down"),
    ("Cosmic Cyclone", 3, "Banishes 1 Spell/Trap"),
    ("Twin Twisters", 3, "Destroys 2 Spell/Traps"),
]

ANTI_HANDTRAPS = [
    ("Called by the Grave", 1, "Banishes from GY and negates"),
    ("Crossout Designator", 3, "Negates card you declare"),
    ("Triple Tactics Talent", 3, "Punishes opponent monster effects in Main Phase"),
]

GOING_FIRST_TRAPS = [
    ("Solemn Judgment", 3, "Negates summon or Spell/Trap"),
    ("Solemn Strike", 3, "Negates monster effect or Special Summon"),
    ("Torrential Tribute", 3, "Destroys all on summon"),
    ("Bottomless Trap Hole", 3, "Banishes 1500+ ATK summon"),
    ("Compulsory Evacuation Device", 3, "Returns 1 monster to hand"),
    ("Ice Dragon's Prison", 3, "Banishes from field/GY"),
]

FLOODGATES = [
    ("Skill Drain", 3, "Negates all face-up monster effects"),
    ("Rivalry of Warlords", 3, "Each player 1 Type only"),
    ("Gozen Match", 3, "Each player 1 Attribute only"),
    ("There Can Be Only One", 3, "Each player 1 of each Type"),
    ("Anti-Spell Fragrance", 3, "Spells must be Set first"),
    ("Macro Cosmos", 3, "All sent cards are banished"),
    ("Dimensional Fissure", 3, "All monsters sent are banished"),
    ("Summon Limit", 3, "2 summons per turn max"),
]

POT_SPELLS = [
    ("Pot of Desires", 3, "Banish 10; draw 2"),
    ("Pot of Extravagance", 3, "Banish Extra Deck; draw 1-2"),
    ("Pot of Prosperity", 3, "Banish Extra Deck; excavate"),
    ("Pot of Duality", 3, "Excavate 3; add 1 (no SS)"),
    ("Upstart Goblin", 1, "Draw 1; opp gains 1000"),
]

EXTRA_DECK_STAPLES = {
    "link": [
        ("Accesscode Talker", 1, "OTK finisher"),
        ("Knightmare Unicorn", 1, "Non-targeting shuffle"),
        ("Knightmare Phoenix", 1, "Spell/Trap pop + draw"),
        ("Knightmare Cerberus", 1, "Monster pop + draw"),
        ("I:P Masquerena", 1, "Link on opponent's turn"),
        ("S:P Little Knight", 1, "Banishes on summon"),
        ("Apollousa, Bow of the Goddess", 1, "Multi-negate"),
        ("Underworld Goddess of the Closed World", 1, "Uses opponent's monster"),
        ("Salamangreat Almiraj", 1, "Link-1 Normal Summon"),
        ("Linkuriboh", 1, "Link-1 Level 1"),
        ("Relinquished Anima", 1, "Link-1 absorb"),
        ("Linguriboh", 1, "Link-1 Trap negate"),
    ],
    "xyz": [
        ("Divine Arsenal AA-ZEUS - Sky Thunder", 1, "Sends all to GY"),
        ("Abyss Dweller", 1, "Negates GY effects"),
        ("Number 41: Bagooska the Terribly Tired Tapir", 1, "Flips/negates"),
        ("Tornado Dragon", 1, "Destroys Spell/Trap"),
        ("Castel, the Skyblaster Musketeer", 1, "Shuffles monster"),
        ("Number 60: Dugares the Timeless", 1, "Draw/ATK/revive"),
        ("Time Thief Redoer", 1, "Steals top deck"),
    ],
    "synchro": [
        ("Baronne de Fleur", 1, "Omni-negate + pop"),
        ("Borreload Savage Dragon", 1, "Monster negate"),
        ("Crystal Wing Synchro Dragon", 1, "Monster negate + ATK"),
        ("PSY-Framelord Omega", 1, "Hand rip + recycle"),
        ("Herald of Arc Light", 1, "Negate + search on GY"),
        ("Stardust Dragon", 1, "Protects from destruction"),
    ],
    "fusion": [
        ("Elder Entity N'tss", 1, "Pops on send to GY"),
        ("Mudragon of the Swamp", 1, "Generic Fusion"),
        ("Starving Venom Fusion Dragon", 1, "Copies effects"),
        ("Predaplant Dragostapelia", 1, "Negates monster effects"),
        ("Garura, Wings of Resonant Life", 1, "Draw on send to GY"),
    ],
}

DECK_RATIOS = {
    "COMBO": {
        "main_deck_size": 40, "monsters": (22, 28), "spells": (10, 16),
        "traps": (0, 4), "handtraps": (6, 12), "starters": (6, 10),
        "extenders": (6, 10), "board_breakers": (0, 3), "extra_deck_size": 15,
    },
    "CONTROL": {
        "main_deck_size": 40, "monsters": (12, 20), "spells": (8, 14),
        "traps": (8, 16), "handtraps": (6, 9), "starters": (4, 8),
        "extenders": (2, 6), "board_breakers": (2, 6), "extra_deck_size": 15,
    },
    "MIDRANGE": {
        "main_deck_size": 40, "monsters": (18, 24), "spells": (10, 14),
        "traps": (4, 10), "handtraps": (6, 12), "starters": (6, 8),
        "extenders": (4, 8), "board_breakers": (2, 4), "extra_deck_size": 15,
    },
    "AGGRO": {
        "main_deck_size": 40, "monsters": (18, 26), "spells": (12, 18),
        "traps": (0, 4), "handtraps": (3, 6), "starters": (6, 10),
        "extenders": (6, 10), "board_breakers": (4, 8), "extra_deck_size": 15,
    },
    "STUN": {
        "main_deck_size": 40, "monsters": (12, 18), "spells": (6, 12),
        "traps": (12, 20), "handtraps": (3, 6), "starters": (4, 8),
        "extenders": (2, 4), "board_breakers": (0, 3), "extra_deck_size": 15,
    },
}

ARCHETYPE_DECK_STYLES: dict[str, str] = {
    "Swordsoul": "MIDRANGE", "Branded": "MIDRANGE", "Despia": "MIDRANGE",
    "Tri-Brigade": "MIDRANGE", "Sky Striker": "CONTROL", "Eldlich": "CONTROL",
    "Altergeist": "CONTROL", "Salamangreat": "MIDRANGE",
    "Adamancipator": "COMBO", "Drytron": "COMBO", "Virtual World": "COMBO",
    "Prank-Kids": "COMBO", "Zoodiac": "MIDRANGE", "Burning Abyss": "MIDRANGE",
    "The Phantom Knights": "COMBO", "Thunder Dragon": "COMBO",
    "Dinosaur": "COMBO", "HERO": "COMBO", "Cyber Dragon": "COMBO",
    "Shaddoll": "MIDRANGE", "Invoked": "CONTROL", "Dark Magician": "CONTROL",
    "Blue-Eyes": "MIDRANGE", "Orcust": "COMBO", "Dogmatika": "CONTROL",
    "Tearlaments": "COMBO", "Kashtira": "CONTROL", "Spright": "COMBO",
    "Marincess": "COMBO", "Labrynth": "CONTROL", "Purrely": "CONTROL",
    "Mathmech": "COMBO", "Runick": "CONTROL", "Rescue-ACE": "CONTROL",
    "Superheavy Samurai": "COMBO", "Centur-Ion": "COMBO",
    "Snake-Eye": "COMBO", "Fiendsmith": "COMBO",
    "Voiceless Voice": "CONTROL", "Tenpai Dragon": "AGGRO",
    "Kaiju": "AGGRO",
}


def get_deck_ratios(style: str) -> dict:
    return DECK_RATIOS.get(style, DECK_RATIOS["MIDRANGE"])


def get_archetype_style(archetype: str) -> str:
    return ARCHETYPE_DECK_STYLES.get(archetype, "MIDRANGE")
