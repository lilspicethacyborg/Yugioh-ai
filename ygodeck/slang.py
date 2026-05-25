"""Yu-Gi-Oh! slang, nicknames, and abbreviation dictionary."""

CARD_NICKNAMES: dict[str, str] = {
    # Hand Traps
    "ash": "Ash Blossom & Joyous Spring", "ash blossom": "Ash Blossom & Joyous Spring",
    "ogre": "Ghost Ogre & Snow Rabbit", "ghost ogre": "Ghost Ogre & Snow Rabbit",
    "belle": "Ghost Belle & Haunted Mansion", "ghost belle": "Ghost Belle & Haunted Mansion",
    "mourner": "Ghost Mourner & Moonlit Chill", "ghost mourner": "Ghost Mourner & Moonlit Chill",
    "veiler": "Effect Veiler",
    "nib": "Nibiru, the Primal Being", "nibiru": "Nibiru, the Primal Being",
    "the rock": "Nibiru, the Primal Being",
    "imperm": "Infinite Impermanence", "imperma": "Infinite Impermanence",
    "impermanence": "Infinite Impermanence",
    "maxx c": "Maxx \"C\"", "maxx": "Maxx \"C\"", "cockroach": "Maxx \"C\"",
    "dd crow": "D.D. Crow", "crow": "D.D. Crow",
    "droll": "Droll & Lock Bird", "droll and lock": "Droll & Lock Bird",
    "lancea": "Artifact Lancea",
    "gamma": "PSY-Framegear Gamma", "psy gamma": "PSY-Framegear Gamma",
    "driver": "PSY-Frame Driver",
    "skull meister": "Skull Meister",
    "d shifter": "Dimension Shifter", "shifter": "Dimension Shifter",
    "dimension shifter": "Dimension Shifter",
    "token collector": "Token Collector",
    "contact c": "Contact \"C\"",
    "fuwalos": "Mulcharmy Fuwalos", "purulia": "Mulcharmy Purulia", "nyalus": "Mulcharmy Nyalus",
    # Staple Spells
    "called by": "Called by the Grave", "cbtg": "Called by the Grave", "called": "Called by the Grave",
    "crossout": "Crossout Designator", "designator": "Crossout Designator",
    "droplet": "Forbidden Droplet", "forbidden droplet": "Forbidden Droplet",
    "chalice": "Forbidden Chalice", "lance": "Forbidden Lance",
    "hfd": "Harpie's Feather Duster", "feather duster": "Harpie's Feather Duster",
    "duster": "Harpie's Feather Duster",
    "raigeki": "Raigeki", "dark hole": "Dark Hole",
    "lightning storm": "Lightning Storm", "lstorm": "Lightning Storm",
    "mst": "Mystical Space Typhoon",
    "twin twister": "Twin Twisters", "twin": "Twin Twisters", "tt": "Twin Twisters",
    "cosmic": "Cosmic Cyclone", "cosmic cyclone": "Cosmic Cyclone",
    "desires": "Pot of Desires", "pot of desires": "Pot of Desires",
    "extrav": "Pot of Extravagance", "extravagance": "Pot of Extravagance",
    "prosperity": "Pot of Prosperity", "prosp": "Pot of Prosperity",
    "upstart": "Upstart Goblin",
    "terraforming": "Terraforming", "terra": "Terraforming",
    "foolish": "Foolish Burial", "foolish goods": "Foolish Burial Goods",
    "one for one": "One for One", "141": "One for One",
    "rota": "Reinforcement of the Army", "reinforcement": "Reinforcement of the Army",
    "e tele": "Emergency Teleport", "emergency teleport": "Emergency Teleport",
    "monster reborn": "Monster Reborn", "reborn": "Monster Reborn",
    "super poly": "Super Polymerization", "super polymerization": "Super Polymerization",
    "book of moon": "Book of Moon", "bom": "Book of Moon",
    "change of heart": "Change of Heart",
    "ttt": "Triple Tactics Talent", "triple tactics": "Triple Tactics Talent",
    "small world": "Small World",
    # Staple Traps
    "judgment": "Solemn Judgment", "solemn j": "Solemn Judgment",
    "solemn judgment": "Solemn Judgment",
    "warning": "Solemn Warning", "solemn warning": "Solemn Warning",
    "strike": "Solemn Strike", "solemn strike": "Solemn Strike",
    "torrential": "Torrential Tribute",
    "bottomless": "Bottomless Trap Hole", "bth": "Bottomless Trap Hole",
    "compulse": "Compulsory Evacuation Device",
    "evenly": "Evenly Matched", "evenly matched": "Evenly Matched",
    "ice d prison": "Ice Dragon's Prison", "ice dragon": "Ice Dragon's Prison",
    "trap trick": "Trap Trick",
    "skill drain": "Skill Drain",
    "rivalry": "Rivalry of Warlords", "gozen": "Gozen Match",
    "tcboo": "There Can Be Only One", "there can be only one": "There Can Be Only One",
    "anti-spell": "Anti-Spell Fragrance", "anti spell": "Anti-Spell Fragrance",
    "imperial order": "Imperial Order", "io": "Imperial Order",
    "vanitys": "Vanity's Emptiness", "vanity's emptiness": "Vanity's Emptiness",
    "macro": "Macro Cosmos", "macro cosmos": "Macro Cosmos",
    "d fissure": "Dimensional Fissure", "dimensional fissure": "Dimensional Fissure",
    # Extra Deck Staples
    "accesscode": "Accesscode Talker", "accesscode talker": "Accesscode Talker",
    "unicorn": "Knightmare Unicorn", "knightmare unicorn": "Knightmare Unicorn",
    "phoenix": "Knightmare Phoenix", "knightmare phoenix": "Knightmare Phoenix",
    "cerberus": "Knightmare Cerberus", "knightmare cerberus": "Knightmare Cerberus",
    "masquerena": "I:P Masquerena", "ip": "I:P Masquerena", "ip masquerena": "I:P Masquerena",
    "baronne": "Baronne de Fleur", "baroness": "Baronne de Fleur",
    "savage": "Borreload Savage Dragon", "borreload savage": "Borreload Savage Dragon",
    "apollousa": "Apollousa, Bow of the Goddess", "apo": "Apollousa, Bow of the Goddess",
    "zeus": "Divine Arsenal AA-ZEUS - Sky Thunder", "aa zeus": "Divine Arsenal AA-ZEUS - Sky Thunder",
    "dweller": "Abyss Dweller", "abyss dweller": "Abyss Dweller",
    "castel": "Castel, the Skyblaster Musketeer",
    "crystal wing": "Crystal Wing Synchro Dragon",
    "omega": "PSY-Framelord Omega",
    "arc light": "Herald of Arc Light",
    "stardust": "Stardust Dragon",
    "underworld goddess": "Underworld Goddess of the Closed World",
    "s:p little knight": "S:P Little Knight", "sp little knight": "S:P Little Knight",
    "little knight": "S:P Little Knight",
    "linkuriboh": "Linkuriboh", "almiraj": "Salamangreat Almiraj",
    "linguriboh": "Linguriboh",
    "ntss": "Elder Entity N'tss", "n'tss": "Elder Entity N'tss",
    "bagooska": "Number 41: Bagooska the Terribly Tired Tapir",
    "winda": "El Shaddoll Winda", "construct": "El Shaddoll Construct",
    "mechaba": "Invoked Mechaba",
    "kagari": "Sky Striker Ace - Kagari", "shizuku": "Sky Striker Ace - Shizuku",
    "hayate": "Sky Striker Ace - Hayate",
    # Game terms -> role markers
    "hand trap": "_ROLE_HANDTRAP", "handtrap": "_ROLE_HANDTRAP",
    "board breaker": "_ROLE_BOARD_BREAKER", "board breakers": "_ROLE_BOARD_BREAKER",
    "floodgate": "_ROLE_FLOODGATE", "staple": "_ROLE_STAPLE", "staples": "_ROLE_STAPLE",
}

ARCHETYPE_ALIASES: dict[str, str] = {
    "salad": "Salamangreat", "salads": "Salamangreat",
    "zoo": "Zoodiac", "ba": "Burning Abyss",
    "pk": "The Phantom Knights", "phantom knights": "The Phantom Knights",
    "vw": "Virtual World", "td": "Thunder Dragon", "thundra": "Thunder Dragon",
    "cydra": "Cyber Dragon", "dm": "Dark Magician",
    "bewd": "Blue-Eyes", "blue eyes": "Blue-Eyes",
    "ss": "Swordsoul", "tri": "Tri-Brigade", "trib": "Tri-Brigade",
    "adam": "Adamancipator", "eld": "Eldlich",
    "dolls": "Shaddoll", "striker": "Sky Striker",
    "pranks": "Prank-Kids", "dogma": "Dogmatika",
    "e hero": "Elemental HERO", "d hero": "Destiny HERO",
    "heroes": "HERO", "heros": "HERO", "hero": "HERO",
    "dino": "Dinosaur", "dinos": "Dinosaur",
    "tear": "Tearlaments", "tears": "Tearlaments",
    "kash": "Kashtira", "lab": "Labrynth",
    "shs": "Superheavy Samurai", "centurion": "Centur-Ion",
    "snake eye": "Snake-Eye", "snake eyes": "Snake-Eye",
    "voiceless": "Voiceless Voice", "tenpai": "Tenpai Dragon",
    "rescue ace": "Rescue-ACE",
}

DECK_STYLE_KEYWORDS: dict[str, str] = {
    "going second": "AGGRO", "go second": "AGGRO",
    "going first": "COMBO", "go first": "COMBO",
    "one turn kill": "AGGRO", "anti-meta": "STUN",
    "anti meta": "STUN", "antimeta": "STUN",
    "combo": "COMBO", "otk": "AGGRO",
    "aggro": "AGGRO", "aggressive": "AGGRO",
    "beatdown": "AGGRO", "rush": "AGGRO",
    "control": "CONTROL", "grind": "CONTROL",
    "trap": "CONTROL",
    "stun": "STUN", "floodgate deck": "STUN",
    "lock": "STUN",
    "midrange": "MIDRANGE", "balanced": "MIDRANGE", "flexible": "MIDRANGE",
}


def resolve_slang(text: str) -> str | None:
    return CARD_NICKNAMES.get(text.strip().lower())


def resolve_archetype_alias(text: str) -> str | None:
    return ARCHETYPE_ALIASES.get(text.strip().lower())


def detect_deck_style(description: str) -> str | None:
    lower = description.lower()
    for keyword, style in DECK_STYLE_KEYWORDS.items():
        if keyword in lower:
            return style
    return None
